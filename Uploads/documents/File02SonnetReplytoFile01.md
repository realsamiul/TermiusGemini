# COMPLETE PIPELINE PLAN

### Tonight's Build — EC2 T4 Large | Qwen + DeepSeek tasking ready

  

---

  

## PART 1: CRICKET DATA — DUAL API, DECIDED

  

**Sportmonks (14-day trial) + CricketData.org ($5.99)**. These two together solve everything cleanly:

  

| Responsibility | Provider |

|---|---|

| Rich metadata — venue, squads, player profiles, flags, tournament info | **Sportmonks** |

| Fast ball-by-ball live polling + scorecard refresh | **CricketData.org** |

| Fallback if either goes down | The other |

  

The logic: Sportmonks has the *depth* (weather, lineups, team images, tournament context). CricketData has the *speed and price* for raw live data. You use Sportmonks once at match start to hydrate the full match context into Redis, then CricketData drives the live tick. This is clean, cheap, and covers the push/pull gap from the earlier discussion.

  

---

  

## PART 2: THE FULL PIPELINE

  

```

MATCH START

    │

    ├── Sportmonks: GET /fixtures/{id}?include=

    │   teams,players,venue,scoreboards,stage,weather

    │   → write full MatchContext to Redis

    │   match:{id}:context  (TTL 24h, static-ish, refresh at toss)

    │

    └── CricketData.org: poll /match-scorecard/{id} every 5s

        → detect delta

        → write MatchState to Redis

        → publish to Centrifugo  →  clients

  

REDIS KEYS

    match:{id}:context     Full Sportmonks enrichment (venue, squads, weather)

    match:{id}:state       Live CricketData scorecard (balls, overs, score)

    match:{id}:events      Redis Stream of ball events (XTRIM 500)

    matches:live           [ match_id, ... ]  TTL 60s

```

  

That's the entire data pipeline. Two sources, three key patterns.

  

---

  

## PART 3: NORMALIZED SCHEMAS

  

Two clean schemas. Everything your frontend ever needs comes from these.

  

### MatchContext (Sportmonks, written once at match start)

  

```typescript

interface MatchContext {

  match_id:     string

  tournament:   string          // "ICC Champions Trophy 2025"

  format:       'T20' | 'ODI' | 'Test'

  venue: {

    name:       string          // "Gaddafi Stadium"

    city:       string

    country:    string

    image_url:  string          // Wikimedia fallback if Sportmonks blank

  }

  team_a: {

    id:         string

    name:       string

    short:      string          // "PAK"

    flag_url:   string          // from Sportmonks flags

  }

  team_b: {

    id:         string

    name:       string

    short:      string

    flag_url:   string

  }

  squads: {

    [team_id: string]: Player[]

  }

  weather: {

    description: string         // "Overcast, chance of rain"

    temp_c:      number

  } | null

  scheduled_start: number       // unix

}

```

  

### MatchState (CricketData, updated every 5s delta)

  

```typescript

interface MatchState {

  match_id:     string

  status:       'upcoming' | 'live' | 'innings_break' | 'completed'

  innings:      number

  team_batting: {

    id:         string

    score:      number

    wickets:    number

    overs:      string          // "32.4"

    run_rate:   number

  }

  team_bowling: {

    id:         string

  }

  striker: {

    id:         string

    name:       string

    runs:       number

    balls:      number

    fours:      number

    sixes:      number

  }

  non_striker: {

    id:         string

    name:       string

    runs:       number

    balls:      number

  }

  bowler: {

    id:         string

    name:       string

    overs:      string

    runs:       number

    wickets:    number

  }

  last_ball: {

    runs:       number

    wicket:     boolean

    extras:     'wide' | 'no-ball' | 'bye' | null

    commentary: string

  }

  target:       number | null

  balls_rem:    number | null

}

```

  

Frontend merges these two: context gives it the venue image, flags, and squad. State gives it everything live. They never need to be mixed server-side — client joins them by `match_id`.

  

---

  

## PART 4: SOCIAL + TRENDING CONTENT PIPELINE

  

Here's the honest state of each source for a free, non-monetised prototype:

  

### X / Twitter — Dead for free API reads

  

The official X API has no free tier for new developers. Pay-per-use is the default: you buy credits upfront and pay per resource, with no free read allowance. Pricing has four tiers: Free ($0 with severe limits), Basic ($100/month for 10K tweets), Pro ($5,000/month for 1M tweets), and Enterprise ($42,000+/month).

  

**What you do instead:** Embed only. X's embed endpoint is free and always has been. You link directly to tweets from official team/board accounts — no API call needed. Your worker curates a hardcoded list of handles, and when a match is live you surface their latest tweet via the public `https://publish.twitter.com/oembed?url=...` endpoint, which is free, requires no key, and returns a render-ready embed HTML block. Fetch this on the worker, push the embed URL as a FeedItem. Done.

  

```typescript

// No API key. No auth. Completely free.

const embed = await fetch(

  `[https://publish.twitter.com/oembed?url=https://twitter.com/${handle}/status/${tweetId}`](https://publish.twitter.com/oembed?url=https://twitter.com/$%7Bhandle%7D/status/$%7BtweetId%7D%60)

)

```

  

### Reddit — Free with OAuth, good enough

  

Reddit's free tier gives you 60 requests per minute with OAuth. For a prototype surfacing r/cricket and r/IPL top posts during a live match, that is more than enough. You can fetch information about specific subreddits including descriptions and subscriber counts, and retrieve posts sorted by hot, new, top, and controversial.

  

You're not storing Reddit data — you're fetching the top 5 posts from r/cricket on each poll cycle, extracting title + URL, and pushing them as link cards into the feed. Reddit does not charge for reasonable use of Reddit Embeds. Link cards are even simpler than embeds.

  

```

Subreddits to poll:

r/cricket, r/IPL, r/CricketShitpost, r/sportsbook (for discourse)

Poll: every 5 minutes (not every second — this is ambient content)

Output: { type: "reddit_link", title, url, score, subreddit }

```

  

**One hard constraint to note:** You cannot display Reddit content and run advertisements within your app. This restriction extends to pre- and post-roll ads, flash overlay ads, paid promotional placements, and all other forms of advertisement. Since your app isn't monetised yet, you're fine. Flag this for when you are.

  

### News Articles — Free via RSS + NewsAPI.org

  

Two tiers:

  

**Cricket-specific RSS (completely free, zero key needed):**

Criczop's RSS feed gives you the opportunity to bring the latest cricket stories to your users at no cost. The feed is completely free. It delivers title, description, and link. The Cricket Feed API only delivers the metadata of news articles such as news title, short description, and time of publication. It does not include the full article body. That's perfect — you want links, not full text.

  

Direct RSS feeds, no API key needed:

```

ESPNcricinfo:     https://www.espncricinfo.com/rss/content/story/feeds/0.xml

CricBuzz:         https://www.cricbuzz.com/rss-feeds/cricket-news

ICC:              https://www.icc-cricket.com/feed

CricTracker:      https://crictracker.com/feed

```

  

**General news fallback — NewsAPI.org:**

NewsAPI is ideal for developers looking to integrate a straightforward newsfeed API. It supports customizable queries and offers data in JSON format. Free developer tier, query `cricket AND {teamA} AND {teamB}`, returns article title + URL + thumbnail. Plenty for a link card.

  

### Meta / Instagram / Facebook — Skip for now

  

Instagram Graph API requires a business account and approved app review. Facebook public post access has been heavily locked since 2018 and requires app review for anything beyond basic profile reads. Neither is worth the friction for a free prototype. What you show instead: if a team's official Instagram posts a reel, it'll surface via their YouTube cross-post or get picked up in news RSS anyway. Skip Meta entirely for now, revisit when you have a monetisation model that justifies the app review process.

  

---

  

## PART 5: COMPLETE WORKER MAP

  

```

worker-live/

  ├── providers/

  │   ├── sportmonks.ts     fetchMatchContext(id) → MatchContext

  │   └── cricketdata.ts    fetchMatchState(id) → MatchState

  ├── loop.ts               poll every 5s, delta check, write Redis, publish Centrifugo

  └── normalizer.ts         raw API → typed schemas

  

worker-media/

  ├── sources/

  │   ├── rss.ts            poll RSS feeds every 3 min → link FeedItems

  │   ├── reddit.ts         poll r/cricket hot posts every 5 min → link FeedItems

  │   ├── youtube.ts        YouTube Data API search → embed FeedItems

  │   └── twitter-embed.ts  oembed fetch for official handles → embed FeedItems

  ├── feed-writer.ts        LPUSH feed:{id}, LTRIM 0 49

  └── scheduler.ts          orchestrates all sources on a per-match basis

```

  

---

  

## PART 6: FEED ITEM SCHEMA (UNIFIED)

  

Every source produces the same shape. Your frontend renders one component regardless of source:

  

```typescript

interface FeedItem {

  id:           string          // uuid

  match_id:     string

  type:         'youtube_embed' | 'tweet_embed' | 'reddit_link' |

                'news_link' | 'remotion_video'

  title:        string          // headline or description

  url:          string          // where user goes on tap

  embed_html:   string | null   // for twitter oembed

  thumbnail:    string | null   // article image or YT thumbnail

  source_name:  string          // "ESPNcricinfo", "r/cricket", "ICC YouTube"

  source_url:   string | null   // attribution link

  created_at:   number

}

```

  

One schema. One feed component. Source-agnostic.

  

---

  

## PART 7: APP STRUCTURE FOR TONIGHT'S TASKING

  

Structure your Qwen/DeepSeek tasks around these discrete, independently completable units:

  

```

TASK 1 — Infrastructure

  docker-compose.yml

  Services: redis:7-alpine, centrifugo:5

  Centrifugo config: token_hmac_secret_key, Redis pub/sub adapter

  Output: both services healthy, centrifugo admin UI accessible

  

TASK 2 — Types Package  [packages/types/]

  MatchContext interface

  MatchState interface

  BallEvent interface

  FeedItem interface

  Export all from index.ts

  

TASK 3 — worker-live  [apps/worker-live/]

  sportmonks.ts: GET /fixtures/{id}?include=teams,venue,weather,players

  cricketdata.ts: GET /match-scorecard/{id}, poll loop

  normalizer.ts: raw → typed schemas

  redis.ts: SET match:{id}:context | SET match:{id}:state | XADD events

  centrifugo.ts: HTTP publish to live-match-{id} channel

  index.ts: orchestrate, delta check, loop

  

TASK 4 — worker-media  [apps/worker-media/]

  rss.ts: fetch + parse 4 RSS feeds, → FeedItem[]

  reddit.ts: OAuth client, GET r/cricket/hot.json, → FeedItem[]

  youtube.ts: YouTube Data API v3 search, filter channel whitelist, → FeedItem[]

  twitter-embed.ts: oembed fetch for hardcoded official handles, → FeedItem[]

  feed-writer.ts: LPUSH + LTRIM + EXPIRE to feed:{match_id}

  scheduler.ts: run each source on its own interval

  

TASK 5 — Frontend hooks only  [apps/frontend/hooks/]

  useLiveMatch(matchId): subscribe Centrifugo, merge context + state

  useFeed(matchId): subscribe Centrifugo live-media channel + initial LRANGE

  Types: consume from packages/types

  NO component styling — hooks only

```

  

Each task is self-contained. Qwen can run Task 2 and Task 3 in parallel. Task 4 depends on Task 2 types. Task 5 depends on Task 2 types + knowing the Centrifugo channel names from Task 3. Hand them in that order.

  

---

  

## WHAT THIS GIVES YOU

  

When all five tasks are done tonight, you have:

  

- **Live scorecard data** flowing from two sources into Redis → Centrifugo → frontend hooks

- **Unified feed** pulling from 4 content sources, all as link cards or embeds, all attributed, all free

- **Clean typed contracts** between every layer so your aesthetic work on components tomorrow plugs straight in without touching the pipeline

- **Zero lock-in** — each worker is independent, each source is a swappable module

  

The aesthetic is entirely yours to build on top. The pipes are sealed.