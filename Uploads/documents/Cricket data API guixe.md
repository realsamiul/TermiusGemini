<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="keywords" content="Cricket score API,live score API,live matches API,cricket API guide,how to get cricket score,cricket how to API,guide for scorecard,CricAPI guide,cricapi how to"><meta name="description" content="Complete API documentation with detailed endpoints, APIs list and input/output data formats for easy consumption"><link rel="icon" href="/img/icon.png"><link rel="apple-touch-icon" href="/img/icon512.png"><meta content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" name="viewport"><meta name="theme-color" content="#FC0203">
    <style>
        pre.code {
            white-space: pre;
            color: #ccc;
            max-height:400px;
            overflow:auto;
        }

            pre.code::before {
                counter-reset: listing;
            }

            pre.code code {
                display: block;
                counter-increment: listing;
            }

                pre.code code::before {
                    content: counter(listing) ".";
                    display: inline-block;
                    background: #0a20a3;
                    color: #ccc;
                    min-width: 2em;
                    padding-left: auto;
                    margin-left: auto;
                    padding-right: 3px;
                    margin-right: 3px;
                    text-align: right;
                }

        pre {
            background: #000;
            color: #fff;
        }

        #sidepan a {
            display: block;
            color: #444;
        }

            #sidepan a b {
                color: #222;
            }

        .string {
            color: #8d8;
        }

        .number {
            color: #23bf3d;
        }

        .boolean {
            color: blue;
        }

        .null {
            color: magenta;
        }

        .key {
            color: #7a9eff;
        }

        div:empty {
            display: none;
        }
    </style>


    <script src="https://cdorg.b-cdn.net/js/jquery-3.6.0.min.js"></script>
    <script>
        // Passive event listeners
        jQuery.event.special.touchstart = {
            setup: function (_, ns, handle) {
                this.addEventListener("touchstart", handle, { passive: !ns.includes("noPreventDefault") });
            }
        };
        jQuery.event.special.touchmove = {
            setup: function (_, ns, handle) {
                this.addEventListener("touchmove", handle, { passive: !ns.includes("noPreventDefault") });
            }
        };
    </script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css" rel="stylesheet">
    <script defer="defer" onload="setTimeout(() =&gt; { if(typeof window.bootReady=='function') window.bootReady();}, 50);" src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js"></script>

    <style>
        * {
            -moz-osx-font-smoothing: grayscale;
            -webkit-font-smoothing: antialiased !important;
            -moz-font-smoothing: antialiased !important;
            text-rendering: optimizelegibility !important;
        }

        .fiv-viv {
            font-size: 1.1em;
            float: left;
            margin-right: 5px;
            line-height: inherit;
        }

        .text-yellow {
            color: gold;
        }

        .text-brown {
            color: brown;
        }
    </style>
    <title>
	Documentation - How to use Cricket Data - CricAPI
</title>

    
    <style>
        body.loading>*:not(#loading) {
            display:none;
        }
        body:not(.loading) #loading {
            display:none;
        }
        body.unloading>*:not(#loading) {
            transition: opacity .25s linear;
            opacity:0;
        }
        body.unloading #loading {
            display:block !important;
            background:rgba(255,255,255,0.5) !important;
        }
        BODY>DIV#loading {
            position:fixed;left:0px;right:0px;top:0px;bottom:0px;
        }
    </style>

    <link rel="canonical" href="https://cricketdata.org/how-to-use-cricket-data-api.aspx"></head>
<body style="background: #fff;" class="">
    <script>
        window.bootReady = function bootReady() {
            var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
        window.addEventListener('load', (event) => {
            $('body').removeClass('loading unloading');
        });
        window.addEventListener('pageshow', (event) => {
            $('body').removeClass('loading unloading');
        });
        window.addEventListener('beforeunload', (event) => {
            $("BODY").removeClass("loading");
            $("BODY").addClass("unloading");
        });
    </script>

    <div id="loading" style="text-align:center;">
        <h1><br><br>Loading...</h1>
        <progress></progress>
    </div>
    

    <nav class="navbar navbar-expand-lg navbar-dark text-white" style="background: #6ab43e">
        <div class="container-fluid">
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <a class="navbar-brand bg-white text-dark px-2" href="/" style="overflow: hidden;position: relative;">
                <img src="/img/icon.png" style="height: 1.5em;">
                <b>Cricket Data</b>
                <span data-bs-toggle="tooltip" data-bs-placement="bottom" title="" alt="Launched 1st May 2022" style="font-size: 8px; float: right; color: black; font-weight: normal; position: absolute; bottom: 1px; right: 10px; text-align: center;" data-bs-original-title="Launched 1st May 2022">Version 1.0</span>
            </a>
            <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    
                    <li class="nav-item">
                        <a class="nav-link" href="/login.aspx">Login</a>
                    </li>
                    
                </ul>
            </div>
        </div>
    </nav>

    <div class="container-fluid" id="mainReplace" style="position: relative">
        <style>
            #topnav {
                border-bottom: 1px rgba(100,100,100,0.5) solid;
            }

            .navbar form {
                display: none !important;
            }


            .buttbutton {
                position: fixed;
                bottom: 30px;
                right: 30px;
                background: #25d388;
                border-radius: 20px;
                width: 40px;
                height: 40px;
                line-height: 35px;
                text-align: center;
                z-index: 5;
            }

                .buttbutton img {
                    width: 32px;
                    height: 32px;
                }

            #sidepan A {
                text-decoration: none
            }


            #topnav .d-none {
                display: none !important;
            }

            #menu a.active {
                color: orange;
                background: #222;
                width: 100%;
            }

            #menu .nav-item {
                width: 100%;
            }

            .alert:empty {
                display: none;
            }
        </style>


        <div class="row">
            
    <div style="position:fixed;z-index:10;top:0px;left:0px;right:0px;padding:7px;text-align:center;background:#800;color:#fff !important;font-weight:bold">To get your Lifetime Free API key <a href="/signup.aspx" class="btn btn-sm btn-primary">signup here</a></div><style>#sidepan,BODY { padding-top:36px; }</style>
    <script>
        window.onscroll = function () {
            if (window.scrollY > 50) {
                sidepan.style.position = "fixed";
                sidepan.style.top = '0';
                sidepan.style.height = '100vh';
                //(window.scrollY - 55) + 'px';
                bodyholderdiv.style.marginLeft = $('#sidepan').outerWidth() + 'px';
            }
            else {
                bodyholderdiv.style.marginLeft = 0;
                sidepan.style.position = "relative";
                sidepan.style.marginTop = 0;
            }
        };
    </script>
    <div id="sidepan" class="d-none d-sm-block col-sm-3 col-md-2 bg-dark" style="min-height: calc(-50px + 100vh); max-height: 100vh; overflow-y: auto; background: rgb(255, 255, 255) !important; position: fixed; margin-top: 0px; top: 0px; height: 100vh;"><a href="#api-generic-information-1"><b>Generic Information</b></a><a href="#api-countries-with-flags-2">Countries with Flags</a><div>&nbsp;</div><a href="#api-list-apis-3"><b>List APIs</b></a><a href="#api-cricket-series-list-4">Cricket Series List</a><a href="#api-cricket-series-search-5">Cricket Series Search</a><a href="#api-all-matches-list-6">All Matches List</a><a href="#api-current-matches-list-7">Current Matches List</a><a href="#api-series-squad-list-8">Series Squad List</a><a href="#api-all-players-list-9">All Players List</a><a href="#api-search-all-players-10">Search All Players</a><div>&nbsp;</div><a href="#api-cricket-info-apis-11"><b>Cricket Info APIs</b></a><a href="#api-series-info-12">Series Info</a><a href="#api-match-info-13">Match Info</a><a href="#api-player-info-14">Player Info</a><div>&nbsp;</div><a href="#api-fantasy-api-15"><b>Fantasy API</b></a></div>
    <div class="col-12 col-sm-9 col-md-10 px-0 px-sm-3 pt-3" id="bodyholderdiv" style="margin-left: 0px;">
        <div class="container-fluid">
            <div class="row" style="min-height: 30vh;" id="bodyrow">
                <div class="col-12">
                    <p>
                        This section explains the basic working of Cricket Data API - it is not 
                    language specific. This can guide you in implementing the API for your favourite programming 
                    language. We also have quite a few <a href="/samples-for-cricket-data-api.aspx">Code Samples</a> 
                        in different languages, - furthermore if you'd like to 
                        contribute please do reach 
                            out to us on contact@cricketdata.org! 
                        The Fantasy APIs may be found <a href="/how-to-use-fantasy-cricket-api.aspx">here</a>.
                    </p>
                    <h2>Index</h2>
                    <div id="APIindex" class="row mb-3"><a class="col-6 col-md-4" href="#api-countries-with-flags-2">Countries with Flags</a><a class="col-6 col-md-4" href="#api-list-apis-3">List APIs</a><a class="col-6 col-md-4" href="#api-cricket-series-list-4">Cricket Series List</a><a class="col-6 col-md-4" href="#api-cricket-series-search-5">Cricket Series Search</a><a class="col-6 col-md-4" href="#api-all-matches-list-6">All Matches List</a><a class="col-6 col-md-4" href="#api-current-matches-list-7">Current Matches List</a><a class="col-6 col-md-4" href="#api-series-squad-list-8">Series Squad List</a><a class="col-6 col-md-4" href="#api-all-players-list-9">All Players List</a><a class="col-6 col-md-4" href="#api-search-all-players-10">Search All Players</a><a class="col-6 col-md-4" href="#api-cricket-info-apis-11">Cricket Info APIs</a><a class="col-6 col-md-4" href="#api-series-info-12">Series Info</a><a class="col-6 col-md-4" href="#api-match-info-13">Match Info</a><a class="col-6 col-md-4" href="#api-player-info-14">Player Info</a><a class="col-6 col-md-4" href="#api-fantasy-api-15">Fantasy API</a></div>
                </div>
            
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-generic-information-1">Generic Information</h2>
<b>Generic API provide you supportive information.</b><br><p>A number of generic API are made available for your use - country, flags, banners and more. Any images / rich content provided is supported by our Global CDN so you can be assured of great performance no matter where you are based.</p><p><b style="color:#800">Important information to remember at all times</b>: Every API response contains a generic 'info' object that tells you the result of your interaction with our systems. JSON keys tagged 'optional' may not exist in some scenarios, so please check for the presence of the key before reading it's value.</p><p><b>Pagination - REMEMBER to correctly provide the 'offset' input parameter.</b> Especially when 'totalRows' are given in the output. Rememeber the default page size is 25 items and if there are more items you will need to change the offset to be able to see them.</p><br><table class="table table-striped explainer"><tbody><tr><th>apikey</th><td><span class="small badge alert-primary">Guid</span> Your subscription's API key. You may use different API keys based on your choice of subscription. <br>This is in a Guid format like 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'.</td></tr> <tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td><span class="small badge alert-primary">Important</span> An array / object containing the main data of the API. Sometimes the response data may have a large number of rows, and it's not possible to send all of them in a single query. One query is limited to 25 rows.</td></tr> <tr><th>info</th><td>An object explaining the result of the API<table class="table table-striped explainer"><tbody><tr><th>hitsToday</th><td><span class="small badge alert-primary">Number</span> Hits made today for the current API Key</td></tr> <tr><th>hitsLimit</th><td><span class="small badge alert-primary">Number</span> Limit on the hits for the current API Key</td></tr> <tr><th>credits</th><td><span class="small badge alert-primary">Number</span> <span class="small badge alert-primary">optional</span> Credits in your account</td></tr> <tr><th>server</th><td><span class="small badge alert-primary">Number</span> The ID of the server that served the current response</td></tr> <tr><th>offsetRows</th><td><span class="small badge alert-primary">Number</span> Row offset, based on what you have requested</td></tr> <tr><th>totalRows</th><td><span class="small badge alert-primary">Number</span> Total rows</td></tr> <tr><th>queryTime</th><td><span class="small badge alert-primary">Number</span> Time (ms) taken to execute the current query</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">10</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">18</span>,</code><code>    <span class="key">"offsetRows":</span> <span class="number">0</span>,</code><code>    <span class="key">"totalRows":</span> <span class="number">249</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">10</span></code><code>  }</code><code>}</code></pre></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-countries-with-flags-2">Countries with Flags</h2>
<b>List of countries and flags</b><br><p>A comprehensive list of all countries with their corresponding flags (served from a CDN in Vector SVG format). Now you can always show flags of the countries that compete in the matches you choose to cover!</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/countries?apikey=[your api key]&amp;offset=0"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing the main data of the API<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">String</span> Unique 2 letter Country ID</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name of the Country</td></tr> <tr><th>genericFlag</th><td><span class="small badge alert-primary">URL</span> URL of the Country's flag (generic)</td></tr> <tr><th>fanartFlag</th><td><span class="small badge alert-primary">URL</span> <span class="small badge alert-primary">optional</span> Fan Art version of the Country's flag</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> [</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"zw"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Zimbabwe"</span>,</code><code>      <span class="key">"genericFlag":</span> <span class="string">"https://cdorg.b-cdn.net/flags/generic/ZW.svg"</span></code><code>    },</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"zm"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Zambia"</span>,</code><code>      <span class="key">"genericFlag":</span> <span class="string">"https://cdorg.b-cdn.net/flags/generic/ZM.svg"</span></code><code>    },</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"za"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"South Africa"</span>,</code><code>      <span class="key">"genericFlag":</span> <span class="string">"https://cdorg.b-cdn.net/flags/generic/ZA.svg"</span></code><code>    }</code><code>  ],</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">10</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">18</span>,</code><code>    <span class="key">"offsetRows":</span> <span class="number">0</span>,</code><code>    <span class="key">"totalRows":</span> <span class="number">249</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">10</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#countries" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div><div class="col-12 mb-5"><hr></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-list-apis-3">List APIs</h2>
<b>These APIs give you a List of items</b><br><p>The common thing to keep in mind is that the 'data' field of the JSON response holds the array of data, and the method for parsing for all List type API is quite similar.</p><br></div>
<div class="col-12 col-md-5 col-lg-4 mb-5"></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-cricket-series-list-4">Cricket Series List</h2>
<b>List of Series covered in Cricket Data</b><br><p>A Descending-Order (latest first) list of all series that we cover. Keep in mind that in some cases series or some matches in the series may only get partial coverage.</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/series?apikey=[your api key]&amp;offset=0"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing the main data of the API<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Series</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name &amp; Year of the Series</td></tr> <tr><th>startDate</th><td><span class="small badge alert-primary">Date</span> Start Date &amp; Month of the Series</td></tr> <tr><th>endDate</th><td><span class="small badge alert-primary">Date</span> End Date &amp; Month of the Series</td></tr> <tr><th>odi</th><td><span class="small badge alert-primary">Number</span> Number of ODIs in this Series</td></tr> <tr><th>t20</th><td><span class="small badge alert-primary">Number</span> Number of T20s in this Series</td></tr> <tr><th>test</th><td><span class="small badge alert-primary">Number</span> Number of Tests in this Series</td></tr> <tr><th>squads</th><td><span class="small badge alert-primary">Number</span> Number of Squads for which data is loaded (series may have more squads for which data is pending / undeclared)</td></tr> <tr><th>matches</th><td><span class="small badge alert-primary">Number</span> Number of Matches for which data is loaded (series may have more matches that are pending / undeclared)</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> [</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"47b54677-34de-4378-9019-154e82b9cc1a"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Indian Premier League 2022"</span>,</code><code>      <span class="key">"startDate":</span> <span class="string">"Mar 26"</span>,</code><code>      <span class="key">"endDate":</span> <span class="string">"May 29"</span>,</code><code>      <span class="key">"odi":</span> <span class="number">0</span>,</code><code>      <span class="key">"t20":</span> <span class="number">70</span>,</code><code>      <span class="key">"test":</span> <span class="number">0</span>,</code><code>      <span class="key">"squads":</span> <span class="number">10</span>,</code><code>      <span class="key">"matches":</span> <span class="number">70</span></code><code>    },</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"ff5aa3f3-7164-4766-be90-3b64783257a0"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Australia Domestic One-Day Cup 2021-22"</span>,</code><code>      <span class="key">"startDate":</span> <span class="string">"Sep 22"</span>,</code><code>      <span class="key">"endDate":</span> <span class="string">"Mar 11"</span>,</code><code>      <span class="key">"odi":</span> <span class="number">19</span>,</code><code>      <span class="key">"t20":</span> <span class="number">0</span>,</code><code>      <span class="key">"test":</span> <span class="number">0</span>,</code><code>      <span class="key">"squads":</span> <span class="number">0</span></code><code>    }</code><code>  ],</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">1</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">18</span>,</code><code>    <span class="key">"offsetRows":</span> <span class="number">0</span>,</code><code>    <span class="key">"totalRows":</span> <span class="number">42</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">10</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#series" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-cricket-series-search-5">Cricket Series Search</h2>
<b>Series Search function for Cricket API</b><br><p>List of all series that match the name specified. This is matches on Name and ShortName. Keep in mind that in some cases series or some matches in the series may only get partial coverage.</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/series?apikey=[your api key]&amp;offset=0&amp;search=IPL"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing the main data of the API<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Series</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name &amp; Year of the Series</td></tr> <tr><th>startDate</th><td><span class="small badge alert-primary">Date</span> Start Date &amp; Month of the Series</td></tr> <tr><th>endDate</th><td><span class="small badge alert-primary">Date</span> End Date &amp; Month of the Series</td></tr> <tr><th>odi</th><td><span class="small badge alert-primary">Number</span> Number of ODIs in this Series</td></tr> <tr><th>t20</th><td><span class="small badge alert-primary">Number</span> Number of T20s in this Series</td></tr> <tr><th>test</th><td><span class="small badge alert-primary">Number</span> Number of Tests in this Series</td></tr> <tr><th>squads</th><td><span class="small badge alert-primary">Number</span> Number of Squads for which data is loaded (series may have more squads for which data is pending / undeclared)</td></tr> <tr><th>matches</th><td><span class="small badge alert-primary">Number</span> Number of Matches for which data is loaded (series may have more matches that are pending / undeclared)</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span>,</code><code>  <span class="key">"search":</span> <span class="string">"IPL"</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> [</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"47b54677-34de-4378-9019-154e82b9cc1a"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Indian Premier League 2022"</span>,</code><code>      <span class="key">"startDate":</span> <span class="string">"Mar 26"</span>,</code><code>      <span class="key">"endDate":</span> <span class="string">"May 29"</span>,</code><code>      <span class="key">"odi":</span> <span class="number">0</span>,</code><code>      <span class="key">"t20":</span> <span class="number">70</span>,</code><code>      <span class="key">"test":</span> <span class="number">0</span>,</code><code>      <span class="key">"squads":</span> <span class="number">10</span>,</code><code>      <span class="key">"matches":</span> <span class="number">70</span></code><code>    }</code><code>  ],</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">1</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">18</span>,</code><code>    <span class="key">"offsetRows":</span> <span class="number">0</span>,</code><code>    <span class="key">"totalRows":</span> <span class="number">42</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">10</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#series" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-all-matches-list-6">All Matches List</h2>
<b>A large list of all matches covered</b><br><p>This API does give you a full list of matches; but keep in mind that using the Series Info API may be easier if you wish to cover just a few series.</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/matches?apikey=[your api key]&amp;offset=0"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing the main data of the API<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Match</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name of the Match</td></tr> <tr><th>matchType</th><td><span class="small badge alert-primary">String</span> Type of the match odi,t20,test</td></tr> <tr><th>score</th><td><span class="small badge alert-primary">Object</span> <span class="small badge alert-primary">optional</span> Score of the match, in inning sequence<br><small><b>Contains</b> Team, Inning, Runs, Wickets, Overs</small></td></tr> <tr><th>status</th><td><span class="small badge alert-primary">String</span> Latest Match status</td></tr> <tr><th>venue</th><td><span class="small badge alert-primary">String</span> Venue of the Match</td></tr> <tr><th>date</th><td><span class="small badge alert-primary">Date</span> Date of the Match</td></tr> <tr><th>dateTimeGMT</th><td><span class="small badge alert-primary">Date</span> Date and Time of the Match in GMT<br>(UTC+00) ISO Format YYYY-MM-DDTHH:mm:ss</td></tr> <tr><th>teams</th><td><span class="small badge alert-primary">Array</span> Names of the teams in JSON array</td></tr> <tr><th>series_id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for the Series this Match is under</td></tr> <tr><th>fantasyEnabled</th><td><span class="small badge alert-primary">Boolean</span> True only if Fantasy Scorecard / Squad / Ball-by-Ball are available for this match</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> [</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"2d448290-d882-4e67-9a4a-f62dfea9a51a"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Western Australia vs New South Wales, Final"</span>,</code><code>      <span class="key">"status":</span> <span class="string">"Western Australia won by 18 runs"</span>,</code><code>      <span class="key">"matchType":</span> <span class="string">"odi"</span>,</code><code>      <span class="key">"venue":</span> <span class="string">"Junction Oval, Melbourne"</span>,</code><code>      <span class="key">"date":</span> <span class="string">"2022-03-10"</span>,</code><code>      <span class="key">"dateTimeGMT":</span> <span class="string">"2022-03-10T23:30:00"</span>,</code><code>      <span class="key">"teams":</span> [</code><code>        <span class="string">"Western Australia"</span>,</code><code>        <span class="string">"New South Wales"</span></code><code>      ],</code><code>      <span class="key">"score":</span> [</code><code>        {</code><code>          <span class="key">"r":</span> <span class="number">207</span>,</code><code>          <span class="key">"w":</span> <span class="number">10</span>,</code><code>          <span class="key">"o":</span> <span class="number">46.3</span>,</code><code>          <span class="key">"inning":</span> <span class="string">"Western Australia Inning 1"</span></code><code>        },</code><code>        {</code><code>          <span class="key">"r":</span> <span class="number">225</span>,</code><code>          <span class="key">"w":</span> <span class="number">9</span>,</code><code>          <span class="key">"o":</span> <span class="number">50</span>,</code><code>          <span class="key">"inning":</span> <span class="string">"New South Wales Inning 1"</span></code><code>        }</code><code>      ],</code><code>      <span class="key">"series_id":</span> <span class="string">"ff5aa3f3-7164-4766-be90-3b64783257a0"</span>,</code><code>      <span class="key">"fantasyEnabled":</span> <span class="boolean">false</span></code><code>    }</code><code>  ],</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">3</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">18</span>,</code><code>    <span class="key">"offsetRows":</span> <span class="number">0</span>,</code><code>    <span class="key">"totalRows":</span> <span class="number">913</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">14.5072</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#matches" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-current-matches-list-7">Current Matches List</h2>
<b>Current matches with a TossWinner but no MatchWinner</b><br><p>This API does give you a full list of CURRENT matches; but keep in mind that using the Series Info API may be easier if you wish to cover just a few series.</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/currentMatches?apikey=[your api key]&amp;offset=0"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing the main data of the API<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Match</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name of the Match</td></tr> <tr><th>matchType</th><td><span class="small badge alert-primary">String</span> Type of the match odi,t20,test</td></tr> <tr><th>score</th><td><span class="small badge alert-primary">Object</span> <span class="small badge alert-primary">optional</span> Score of the match, in inning sequence<br><small><b>Contains</b> Team, Inning, Runs, Wickets, Overs</small></td></tr> <tr><th>status</th><td><span class="small badge alert-primary">String</span> Latest Match status</td></tr> <tr><th>venue</th><td><span class="small badge alert-primary">String</span> Venue of the Match</td></tr> <tr><th>date</th><td><span class="small badge alert-primary">Date</span> Date of the Match</td></tr> <tr><th>dateTimeGMT</th><td><span class="small badge alert-primary">Date</span> Date and Time of the Match in GMT<br>(UTC+00) ISO Format YYYY-MM-DDTHH:mm:ss</td></tr> <tr><th>teams</th><td><span class="small badge alert-primary">Array</span> Names of the teams in JSON array</td></tr> <tr><th>series_id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for the Series this Match is under</td></tr> <tr><th>fantasyEnabled</th><td><span class="small badge alert-primary">Boolean</span> True only if Fantasy Scorecard / Squad / Ball-by-Ball are available for this match</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> [</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"2d448290-d882-4e67-9a4a-f62dfea9a51a"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Western Australia vs New South Wales, Final"</span>,</code><code>      <span class="key">"status":</span> <span class="string">"Western Australia won by 18 runs"</span>,</code><code>      <span class="key">"matchType":</span> <span class="string">"odi"</span>,</code><code>      <span class="key">"venue":</span> <span class="string">"Junction Oval, Melbourne"</span>,</code><code>      <span class="key">"date":</span> <span class="string">"2022-03-10"</span>,</code><code>      <span class="key">"dateTimeGMT":</span> <span class="string">"2022-03-10T23:30:00"</span>,</code><code>      <span class="key">"teams":</span> [</code><code>        <span class="string">"Western Australia"</span>,</code><code>        <span class="string">"New South Wales"</span></code><code>      ],</code><code>      <span class="key">"score":</span> [</code><code>        {</code><code>          <span class="key">"r":</span> <span class="number">207</span>,</code><code>          <span class="key">"w":</span> <span class="number">10</span>,</code><code>          <span class="key">"o":</span> <span class="number">46.3</span>,</code><code>          <span class="key">"inning":</span> <span class="string">"Western Australia Inning 1"</span></code><code>        },</code><code>        {</code><code>          <span class="key">"r":</span> <span class="number">225</span>,</code><code>          <span class="key">"w":</span> <span class="number">9</span>,</code><code>          <span class="key">"o":</span> <span class="number">50</span>,</code><code>          <span class="key">"inning":</span> <span class="string">"New South Wales Inning 1"</span></code><code>        }</code><code>      ],</code><code>      <span class="key">"series_id":</span> <span class="string">"ff5aa3f3-7164-4766-be90-3b64783257a0"</span>,</code><code>      <span class="key">"fantasyEnabled":</span> <span class="boolean">false</span></code><code>    }</code><code>  ],</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">3</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">18</span>,</code><code>    <span class="key">"offsetRows":</span> <span class="number">0</span>,</code><code>    <span class="key">"totalRows":</span> <span class="number">913</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">14.5072</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#currentMatches" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-series-squad-list-8">Series Squad List</h2>
<b>Coming soon</b><br><p>The Series squad list API gives you a list of Squads in the given Series. This is yet under development, so please bear with us. Coming soon!</p><br></div>
<div class="col-12 col-md-5 col-lg-4 mb-5"></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-all-players-list-9">All Players List</h2>
<b>A large list of all players in the system</b><br><p>This API gives you a full list of players with their Country of origin. Based on this you can then query the Player Info API and get more details for each player.</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/players?apikey=[your api key]&amp;offset=0"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing the main data of the API<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Player</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Full Name of the player</td></tr> <tr><th>country</th><td><span class="small badge alert-primary">String</span> Country the player belongs to</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> [</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"16592242-ef26-45d9-bf23-fc090e90fbbe"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Anderson Phillip"</span>,</code><code>      <span class="key">"country":</span> <span class="string">"West Indies"</span></code><code>    },</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"9f2abfee-a09f-47c8-a1e5-8eb03fa7b85a"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Veerasammy Permaul"</span>,</code><code>      <span class="key">"country":</span> <span class="string">"West Indies"</span></code><code>    }</code><code>  ],</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">7</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">18</span>,</code><code>    <span class="key">"offsetRows":</span> <span class="number">0</span>,</code><code>    <span class="key">"totalRows":</span> <span class="number">1992</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">10.099</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#matches" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-search-all-players-10">Search All Players</h2>
<b>Searches through our entire players database in the system</b><br><p>This API gives you a full list of players with their Country of origin. Based on this you can then query the Player Info API and get more details for each player.</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/players?apikey=[your api key]&amp;offset=0"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing the main data of the API<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Player</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Full Name of the player</td></tr> <tr><th>country</th><td><span class="small badge alert-primary">String</span> Country the player belongs to</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> [</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"16592242-ef26-45d9-bf23-fc090e90fbbe"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Anderson Phillip"</span>,</code><code>      <span class="key">"country":</span> <span class="string">"West Indies"</span></code><code>    },</code><code>    {</code><code>      <span class="key">"id":</span> <span class="string">"9f2abfee-a09f-47c8-a1e5-8eb03fa7b85a"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Veerasammy Permaul"</span>,</code><code>      <span class="key">"country":</span> <span class="string">"West Indies"</span></code><code>    }</code><code>  ],</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">7</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">18</span>,</code><code>    <span class="key">"offsetRows":</span> <span class="number">0</span>,</code><code>    <span class="key">"totalRows":</span> <span class="number">1992</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">10.099</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#matches" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div><div class="col-12 mb-5"><hr></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-cricket-info-apis-11">Cricket Info APIs</h2>
<b>These APIs give you Details of each item shown in the List API</b><br><p>Details about series, matches, players, etc can be acquired through this API. Keep in mind that this API does NOT have pagination, so if there's a long list or a large API response you will need to handle it accordingly.</p><br></div>
<div class="col-12 col-md-5 col-lg-4 mb-5"></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-series-info-12">Series Info</h2>
<b>Detailed info about the Series</b><br><p>Based on the Series ID provided, this API will give you information about the Series. Beware that the Match List given here is the COMPLETE list, so it will be very HEAVY when the Series has a large number of matches! You should ideally pull this API max 2-3 times a Day or on Manual intervention from your end if required.</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/series_info?apikey=[your api key]&amp;offset=0&amp;id=47b54677-34de-4378-9019-154e82b9cc1a"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing the main data of the API<table class="table table-striped explainer"><tbody><tr><th>info</th><td>The basic details about the Series<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Series</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name &amp; Year of the Series</td></tr> <tr><th>startDate</th><td><span class="small badge alert-primary">Date</span> Start Date &amp; Month of the Series</td></tr> <tr><th>endDate</th><td><span class="small badge alert-primary">Date</span> End Date &amp; Month of the Series</td></tr> <tr><th>odi</th><td><span class="small badge alert-primary">Number</span> Number of ODIs in this Series</td></tr> <tr><th>t20</th><td><span class="small badge alert-primary">Number</span> Number of T20s in this Series</td></tr> <tr><th>test</th><td><span class="small badge alert-primary">Number</span> Number of Tests in this Series</td></tr> <tr><th>squads</th><td><span class="small badge alert-primary">Number</span> Number of Squads for which data is loaded (series may have more squads for which data is pending / undeclared)</td></tr> <tr><th>matches</th><td><span class="small badge alert-primary">Number</span> Number of Matches for which data is loaded (series may have more matches that are pending / undeclared)</td></tr></tbody></table></td></tr> <tr><th>matchList</th><td>An array / object containing the Matches in this Series<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Match</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name of the MAtch</td></tr> <tr><th>matchType</th><td><span class="small badge alert-primary">String</span> Type of the match odi,t20,test</td></tr> <tr><th>status</th><td><span class="small badge alert-primary">String</span> Latest Match status</td></tr> <tr><th>venue</th><td><span class="small badge alert-primary">String</span> Venue of the Match</td></tr> <tr><th>date</th><td><span class="small badge alert-primary">Date</span> Date of the Match</td></tr> <tr><th>dateTimeGMT</th><td><span class="small badge alert-primary">Date</span> Date and Time of the Match in GMT<br>(UTC+00) ISO Format YYYY-MM-DDTHH:mm:ss</td></tr> <tr><th>teams</th><td><span class="small badge alert-primary">Array</span> Names of the teams in JSON array</td></tr> <tr><th>fantasyEnabled</th><td><span class="small badge alert-primary">Boolean</span> True only if Fantasy Scorecard / Squad / Ball-by-Ball are available for this match</td></tr></tbody></table></td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span>,</code><code>  <span class="key">"id":</span> <span class="string">"47b54677-34de-4378-9019-154e82b9cc1a"</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> {</code><code>    <span class="key">"info":</span> {</code><code>      <span class="key">"id":</span> <span class="string">"47b54677-34de-4378-9019-154e82b9cc1a"</span>,</code><code>      <span class="key">"name":</span> <span class="string">"Indian Premier League 2022"</span>,</code><code>      <span class="key">"startdate":</span> <span class="string">"Mar 26"</span>,</code><code>      <span class="key">"enddate":</span> <span class="string">"May 29"</span>,</code><code>      <span class="key">"odi":</span> <span class="number">0</span>,</code><code>      <span class="key">"t20":</span> <span class="number">70</span>,</code><code>      <span class="key">"test":</span> <span class="number">0</span>,</code><code>      <span class="key">"squads":</span> <span class="number">10</span>,</code><code>      <span class="key">"matches":</span> <span class="number">70</span></code><code>    },</code><code>    <span class="key">"matchList":</span> [</code><code>      {</code><code>        <span class="key">"id":</span> <span class="string">"341e6690-ece0-4dce-83fc-91effbb28eb3"</span>,</code><code>        <span class="key">"name":</span> <span class="string">"Chennai Super Kings vs Kolkata Knight Riders, 1st Match"</span>,</code><code>        <span class="key">"matchType":</span> <span class="string">"t20"</span>,</code><code>        <span class="key">"status":</span> <span class="string">"Match not started"</span>,</code><code>        <span class="key">"venue":</span> <span class="string">"Wankhede Stadium, Mumbai"</span>,</code><code>        <span class="key">"date":</span> <span class="string">"2022-03-26"</span>,</code><code>        <span class="key">"dateTimeGMT":</span> <span class="string">"2022-03-26T14:00:00"</span>,</code><code>        <span class="key">"teams":</span> [</code><code>          <span class="string">"Chennai Super Kings"</span>,</code><code>          <span class="string">"Kolkata Knight Riders"</span></code><code>        ],</code><code>        <span class="key">"fantasyEnabled":</span> <span class="boolean">false</span></code><code>      }</code><code>    ]</code><code>  },</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">12</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">11</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">10</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#series_info" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-match-info-13">Match Info</h2>
<b>Detailed info about the Match</b><br><p>Provides the details of this cricket match. If you require scorecard / ball by ball or other more detailed information, please use the corresponding Fantasy Squad / Fantasy Scorecard / Fantasy Ball-by-Ball API.</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/match_info?apikey=[your api key]&amp;offset=0&amp;id=820cfd88-3b56-4a6e-9dd8-1203051140da"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing this Matches detail<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Match</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name of the Match</td></tr> <tr><th>matchType</th><td><span class="small badge alert-primary">String</span> Type of the match odi,t20,test</td></tr> <tr><th>score</th><td><span class="small badge alert-primary">Object</span> <span class="small badge alert-primary">optional</span> Score of the match, in inning sequence<br><small><b>Contains</b> Team, Inning, Runs, Wickets, Overs</small></td></tr> <tr><th>status</th><td><span class="small badge alert-primary">String</span> Latest Match status</td></tr> <tr><th>venue</th><td><span class="small badge alert-primary">String</span> Venue of the Match</td></tr> <tr><th>date</th><td><span class="small badge alert-primary">Date</span> Date of the Match</td></tr> <tr><th>dateTimeGMT</th><td><span class="small badge alert-primary">Date</span> Date and Time of the Match in GMT<br>(UTC+00) ISO Format YYYY-MM-DDTHH:mm:ss</td></tr> <tr><th>teams</th><td><span class="small badge alert-primary">Array</span> Names of the teams in JSON array</td></tr> <tr><th>fantasyEnabled</th><td><span class="small badge alert-primary">Boolean</span> True only if Fantasy Scorecard / Squad / Ball-by-Ball are available for this match</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span>,</code><code>  <span class="key">"id":</span> <span class="string">"820cfd88-3b56-4a6e-9dd8-1203051140da"</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> {</code><code>    <span class="key">"id":</span> <span class="string">"2d448290-d882-4e67-9a4a-f62dfea9a51a"</span>,</code><code>    <span class="key">"name":</span> <span class="string">"Western Australia vs New South Wales, Final"</span>,</code><code>    <span class="key">"matchType":</span> <span class="string">"odi"</span>,</code><code>    <span class="key">"status":</span> <span class="string">"Western Australia won by 18 runs"</span>,</code><code>    <span class="key">"venue":</span> <span class="string">"Junction Oval, Melbourne"</span>,</code><code>    <span class="key">"date":</span> <span class="string">"2022-03-10"</span>,</code><code>    <span class="key">"dateTimeGMT":</span> <span class="string">"2022-03-10T23:30:00"</span>,</code><code>    <span class="key">"teams":</span> [</code><code>      <span class="string">"Western Australia"</span>,</code><code>      <span class="string">"New South Wales"</span></code><code>    ],</code><code>    <span class="key">"score":</span> [</code><code>      {</code><code>        <span class="key">"r":</span> <span class="number">207</span>,</code><code>        <span class="key">"w":</span> <span class="number">10</span>,</code><code>        <span class="key">"o":</span> <span class="number">46.3</span>,</code><code>        <span class="key">"inning":</span> <span class="string">"Western Australia Inning 1"</span></code><code>      },</code><code>      {</code><code>        <span class="key">"r":</span> <span class="number">225</span>,</code><code>        <span class="key">"w":</span> <span class="number">9</span>,</code><code>        <span class="key">"o":</span> <span class="number">50</span>,</code><code>        <span class="key">"inning":</span> <span class="string">"New South Wales Inning 1"</span></code><code>      }</code><code>    ],</code><code>    <span class="key">"tossWinner":</span> <span class="string">"Western Australia"</span>,</code><code>    <span class="key">"tossChoice":</span> <span class="string">"bat"</span>,</code><code>    <span class="key">"matchWinner":</span> <span class="string">"Western Australia"</span>,</code><code>    <span class="key">"series_id":</span> <span class="string">"ff5aa3f3-7164-4766-be90-3b64783257a0"</span>,</code><code>    <span class="key">"fantasyEnabled":</span> <span class="boolean">false</span></code><code>  },</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">21</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">11</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">15.7629</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#match_info" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-player-info-14">Player Info</h2>
<b>Detailed info about the Player</b><br><p>Basic details about the player are provided in this API. In future we will include a player photograph (coming soon).</p><br><input type="text" class="form-control" readonly="" value="https://api.cricapi.com/v1/players_info?apikey=[your api key]&amp;offset=0&amp;id=16592242-ef26-45d9-bf23-fc090e90fbbe"><br><table class="table table-striped explainer"><tbody><tr><th>status</th><td><span class="small badge alert-primary">String</span> success / failure based on the API result</td></tr> <tr><th>data</th><td>An array / object containing this Player detail<table class="table table-striped explainer"><tbody><tr><th>id</th><td><span class="small badge alert-primary">Guid</span> Unique identifier for this Player</td></tr> <tr><th>name</th><td><span class="small badge alert-primary">String</span> Name of the Player</td></tr> <tr><th>dateOfBirth</th><td><span class="small badge alert-primary">Date</span> Date of Birth</td></tr> <tr><th>role</th><td><span class="small badge alert-primary">String</span> Player's Role</td></tr> <tr><th>battingStyle</th><td><span class="small badge alert-primary">String</span> Batting Style</td></tr> <tr><th>bowlingStyle</th><td><span class="small badge alert-primary">String</span> Bowling Style</td></tr> <tr><th>placeOfBirth</th><td><span class="small badge alert-primary">String</span> Place of Birth</td></tr> <tr><th>country</th><td><span class="small badge alert-primary">String</span> Player's Country</td></tr></tbody></table></td></tr></tbody></table></div>
<div class="col-12 col-md-5 col-lg-4 mb-5">Input<br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"offset":</span> <span class="number">0</span>,</code><code>  <span class="key">"id":</span> <span class="string">"16592242-ef26-45d9-bf23-fc090e90fbbe"</span></code><code>}</code></pre>Output<br><small>(data may be truncated for ease of reading)</small><br><pre class="code"><code>{</code><code>  <span class="key">"apikey":</span> <span class="string">"[your api key]"</span>,</code><code>  <span class="key">"data":</span> {</code><code>    <span class="key">"id":</span> <span class="string">"16592242-ef26-45d9-bf23-fc090e90fbbe"</span>,</code><code>    <span class="key">"name":</span> <span class="string">"Anderson Phillip"</span>,</code><code>    <span class="key">"dateOfBirth":</span> <span class="string">"1996-08-22T00:00:00"</span>,</code><code>    <span class="key">"role":</span> <span class="string">"Bowler"</span>,</code><code>    <span class="key">"battingStyle":</span> <span class="string">"Right Handed Bat"</span>,</code><code>    <span class="key">"bowlingStyle":</span> <span class="string">"Right-arm fast-medium"</span>,</code><code>    <span class="key">"placeOfBirth":</span> <span class="string">"--"</span>,</code><code>    <span class="key">"country":</span> <span class="string">"West Indies"</span></code><code>  },</code><code>  <span class="key">"status":</span> <span class="string">"success"</span>,</code><code>  <span class="key">"info":</span> {</code><code>    <span class="key">"hitsToday":</span> <span class="number">41</span>,</code><code>    <span class="key">"hitsLimit":</span> <span class="number">500</span>,</code><code>    <span class="key">"credits":</span> <span class="number">0</span>,</code><code>    <span class="key">"server":</span> <span class="number">11</span>,</code><code>    <span class="key">"queryTime":</span> <span class="number">10</span></code><code>  }</code><code>}</code></pre><center>Try out the API in real time<br> 
<a href="/member-test.aspx#players_info" class="btn btn-sm btn-success">Code Playground 
<i class="fa fa-arrow-right"></i></a></center></div><div class="col-12 mb-5"><hr></div>
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id="api-fantasy-api-15">Fantasy API</h2>
<span class="badge bg-success">Work in Progress</span> <b>Detailed Scorecard, Squad and Ball-By-Ball APIs</b><br><p>Fantasy API includes Scorecard, Ball-by-Ball and Squad API for each match. This is still a work in progress, so expect more changes to come in the future!</p><center><a class="btn btn-lg btn-success" href="/how-to-use-fantasy-cricket-api.aspx">Get the Fantasy APIs (Scorecard, Squad, Ball-By-Ball, Points, etc) here</a></center><br></div>
<div class="col-12 col-md-5 col-lg-4 mb-5"></div></div>
        </div>
    </div>
    <style>
        .explainer .badge {
            font-size:0.7em;
            text-transform:capitalize;
        }
        .explainer *:not(.badge) {
            vertical-align:top;
        }

        .explainer.table-striped>tbody>tr:nth-of-type(even) {
            background:#fff !important;
        }
        .explainer.table-striped>tbody>tr:nth-of-type(odd) {
            background:#fefeff !important;
        }

        @media only screen and (max-width: 600px) {
            #APIindex a {
                display: block;
                margin-bottom: 5px;
                margin-top: 5px;
            }
        }
    </style>
    <script>

        let uid = 0;

        $(function () {
            let x = [
  {
    "bold": 1,
    "title": "Generic Information",
    "info": "<b>Generic API provide you supportive information.</b><Br><p>A number of generic API are made available for your use - country, flags, banners and more. Any images / rich content provided is supported by our Global CDN so you can be assured of great performance no matter where you are based.</p><p><b style='color:#800'>Important information to remember at all times</b>: Every API response contains a generic 'info' object that tells you the result of your interaction with our systems. JSON keys tagged 'optional' may not exist in some scenarios, so please check for the presence of the key before reading it's value.</p><p><b>Pagination - REMEMBER to correctly provide the 'offset' input parameter.</b> Especially when 'totalRows' are given in the output. Rememeber the default page size is 25 items and if there are more items you will need to change the offset to be able to see them.</p>",
    "output": {
      "apikey": "%APIKEY%",
      "status": "success",
      "info": {
        "hitsToday": 10,
        "hitsLimit": 500,
        "credits": 0,
        "server": 18,
        "offsetRows": 0,
        "totalRows": 249,
        "queryTime": 10
      }
    },
    "explain": {
      "apikey": "Guid:Your subscription's API key. You may use different API keys based on your choice of subscription. <br>This is in a Guid format like 'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'.",
      "status": "String:success / failure based on the API result",
      "data": "Important:An array / object containing the main data of the API. Sometimes the response data may have a large number of rows, and it's not possible to send all of them in a single query. One query is limited to 25 rows.",
      "info": {
        "~": "An object explaining the result of the API",
        "hitsToday": "Number:Hits made today for the current API Key",
        "hitsLimit": "Number:Limit on the hits for the current API Key",
        "credits": "Number,optional:Credits in your account",
        "server": "Number:The ID of the server that served the current response",
        "offsetRows": "Number:Row offset, based on what you have requested",
        "totalRows": "Number:Total rows",
        "queryTime": "Number:Time (ms) taken to execute the current query"
      }
    }
  },
  {
    "bold": 0,
    "title": "Countries with Flags",
    "info": "<b>List of countries and flags</b><Br><p>A comprehensive list of all countries with their corresponding flags (served from a CDN in Vector SVG format). Now you can always show flags of the countries that compete in the matches you choose to cover!</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing the main data of the API",
        "id": "String:Unique 2 letter Country ID",
        "name": "String:Name of the Country",
        "genericFlag": "URL:URL of the Country's flag (generic)",
        "fanartFlag": "URL,optional:Fan Art version of the Country's flag"
      }
    },
    "endpoint": "v1/countries?apikey=%APIKEY%&offset=0",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": [
        {
          "id": "zw",
          "name": "Zimbabwe",
          "genericFlag": "https://cdorg.b-cdn.net/flags/generic/ZW.svg"
        },
        {
          "id": "zm",
          "name": "Zambia",
          "genericFlag": "https://cdorg.b-cdn.net/flags/generic/ZM.svg"
        },
        {
          "id": "za",
          "name": "South Africa",
          "genericFlag": "https://cdorg.b-cdn.net/flags/generic/ZA.svg"
        }
      ],
      "status": "success",
      "info": {
        "hitsToday": 10,
        "hitsLimit": 500,
        "credits": 0,
        "server": 18,
        "offsetRows": 0,
        "totalRows": 249,
        "queryTime": 10
      }
    },
    "playground": "#countries"
  },
  {},
  {
    "bold": 1,
    "title": "List APIs",
    "info": "<b>These APIs give you a List of items</b><Br><p>The common thing to keep in mind is that the 'data' field of the JSON response holds the array of data, and the method for parsing for all List type API is quite similar.</p>"
  },
  {
    "bold": 0,
    "title": "Cricket Series List",
    "info": "<b>List of Series covered in Cricket Data</b><Br><p>A Descending-Order (latest first) list of all series that we cover. Keep in mind that in some cases series or some matches in the series may only get partial coverage.</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing the main data of the API",
        "id": "Guid:Unique identifier for this Series",
        "name": "String:Name & Year of the Series",
        "startDate": "Date:Start Date & Month of the Series",
        "endDate": "Date:End Date & Month of the Series",
        "odi": "Number:Number of ODIs in this Series",
        "t20": "Number:Number of T20s in this Series",
        "test": "Number:Number of Tests in this Series",
        "squads": "Number:Number of Squads for which data is loaded (series may have more squads for which data is pending / undeclared)",
        "matches": "Number:Number of Matches for which data is loaded (series may have more matches that are pending / undeclared)"
      }
    },
    "endpoint": "v1/series?apikey=%APIKEY%&offset=0",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": [
        {
          "id": "47b54677-34de-4378-9019-154e82b9cc1a",
          "name": "Indian Premier League 2022",
          "startDate": "Mar 26",
          "endDate": "May 29",
          "odi": 0,
          "t20": 70,
          "test": 0,
          "squads": 10,
          "matches": 70
        },
        {
          "id": "ff5aa3f3-7164-4766-be90-3b64783257a0",
          "name": "Australia Domestic One-Day Cup 2021-22",
          "startDate": "Sep 22",
          "endDate": "Mar 11",
          "odi": 19,
          "t20": 0,
          "test": 0,
          "squads": 0
        }
      ],
      "status": "success",
      "info": {
        "hitsToday": 1,
        "hitsLimit": 500,
        "credits": 0,
        "server": 18,
        "offsetRows": 0,
        "totalRows": 42,
        "queryTime": 10
      }
    },
    "playground": "#series"
  },
  {
    "bold": 0,
    "title": "Cricket Series Search",
    "info": "<b>Series Search function for Cricket API</b><Br><p>List of all series that match the name specified. This is matches on Name and ShortName. Keep in mind that in some cases series or some matches in the series may only get partial coverage.</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing the main data of the API",
        "id": "Guid:Unique identifier for this Series",
        "name": "String:Name & Year of the Series",
        "startDate": "Date:Start Date & Month of the Series",
        "endDate": "Date:End Date & Month of the Series",
        "odi": "Number:Number of ODIs in this Series",
        "t20": "Number:Number of T20s in this Series",
        "test": "Number:Number of Tests in this Series",
        "squads": "Number:Number of Squads for which data is loaded (series may have more squads for which data is pending / undeclared)",
        "matches": "Number:Number of Matches for which data is loaded (series may have more matches that are pending / undeclared)"
      }
    },
    "endpoint": "v1/series?apikey=%APIKEY%&offset=0&search=IPL",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0,
      "search": "IPL"
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": [
        {
          "id": "47b54677-34de-4378-9019-154e82b9cc1a",
          "name": "Indian Premier League 2022",
          "startDate": "Mar 26",
          "endDate": "May 29",
          "odi": 0,
          "t20": 70,
          "test": 0,
          "squads": 10,
          "matches": 70
        }
      ],
      "status": "success",
      "info": {
        "hitsToday": 1,
        "hitsLimit": 500,
        "credits": 0,
        "server": 18,
        "offsetRows": 0,
        "totalRows": 42,
        "queryTime": 10
      }
    },
    "playground": "#series"
  },
  {
    "bold": 0,
    "title": "All Matches List",
    "info": "<b>A large list of all matches covered</b><Br><p>This API does give you a full list of matches; but keep in mind that using the Series Info API may be easier if you wish to cover just a few series.</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing the main data of the API",
        "id": "Guid:Unique identifier for this Match",
        "name": "String:Name of the Match",
        "matchType": "String:Type of the match odi,t20,test",
        "score": "Object,optional:Score of the match, in inning sequence<Br/><small><b>Contains</b> Team, Inning, Runs, Wickets, Overs</small>",
        "status": "String:Latest Match status",
        "venue": "String:Venue of the Match",
        "date": "Date:Date of the Match",
        "dateTimeGMT": "Date:Date and Time of the Match in GMT<Br/>(UTC+00) ISO Format YYYY-MM-DDTHH&#58;mm&#58;ss",
        "teams": "Array:Names of the teams in JSON array",
        "series_id": "Guid:Unique identifier for the Series this Match is under",
        "fantasyEnabled": "Boolean:True only if Fantasy Scorecard / Squad / Ball-by-Ball are available for this match"
      }
    },
    "endpoint": "v1/matches?apikey=%APIKEY%&offset=0",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": [
        {
          "id": "2d448290-d882-4e67-9a4a-f62dfea9a51a",
          "name": "Western Australia vs New South Wales, Final",
          "status": "Western Australia won by 18 runs",
          "matchType": "odi",
          "venue": "Junction Oval, Melbourne",
          "date": "2022-03-10",
          "dateTimeGMT": "2022-03-10T23:30:00",
          "teams": [ "Western Australia", "New South Wales" ],
          "score": [
            {
              "r": 207,
              "w": 10,
              "o": 46.3,
              "inning": "Western Australia Inning 1"
            },
            {
              "r": 225,
              "w": 9,
              "o": 50,
              "inning": "New South Wales Inning 1"
            }
          ],
          "series_id": "ff5aa3f3-7164-4766-be90-3b64783257a0",
          "fantasyEnabled": false
        }
      ],
      "status": "success",
      "info": {
        "hitsToday": 3,
        "hitsLimit": 500,
        "credits": 0,
        "server": 18,
        "offsetRows": 0,
        "totalRows": 913,
        "queryTime": 14.5072
      }
    },
    "playground": "#matches"
  },
  {
    "bold": 0,
    "title": "Current Matches List",
    "info": "<b>Current matches with a TossWinner but no MatchWinner</b><Br><p>This API does give you a full list of CURRENT matches; but keep in mind that using the Series Info API may be easier if you wish to cover just a few series.</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing the main data of the API",
        "id": "Guid:Unique identifier for this Match",
        "name": "String:Name of the Match",
        "matchType": "String:Type of the match odi,t20,test",
        "score": "Object,optional:Score of the match, in inning sequence<Br/><small><b>Contains</b> Team, Inning, Runs, Wickets, Overs</small>",
        "status": "String:Latest Match status",
        "venue": "String:Venue of the Match",
        "date": "Date:Date of the Match",
        "dateTimeGMT": "Date:Date and Time of the Match in GMT<Br/>(UTC+00) ISO Format YYYY-MM-DDTHH&#58;mm&#58;ss",
        "teams": "Array:Names of the teams in JSON array",
        "series_id": "Guid:Unique identifier for the Series this Match is under",
        "fantasyEnabled": "Boolean:True only if Fantasy Scorecard / Squad / Ball-by-Ball are available for this match"
      }
    },
    "endpoint": "v1/currentMatches?apikey=%APIKEY%&offset=0",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": [
        {
          "id": "2d448290-d882-4e67-9a4a-f62dfea9a51a",
          "name": "Western Australia vs New South Wales, Final",
          "status": "Western Australia won by 18 runs",
          "matchType": "odi",
          "venue": "Junction Oval, Melbourne",
          "date": "2022-03-10",
          "dateTimeGMT": "2022-03-10T23:30:00",
          "teams": [ "Western Australia", "New South Wales" ],
          "score": [
            {
              "r": 207,
              "w": 10,
              "o": 46.3,
              "inning": "Western Australia Inning 1"
            },
            {
              "r": 225,
              "w": 9,
              "o": 50,
              "inning": "New South Wales Inning 1"
            }
          ],
          "series_id": "ff5aa3f3-7164-4766-be90-3b64783257a0",
          "fantasyEnabled": false
        }
      ],
      "status": "success",
      "info": {
        "hitsToday": 3,
        "hitsLimit": 500,
        "credits": 0,
        "server": 18,
        "offsetRows": 0,
        "totalRows": 913,
        "queryTime": 14.5072
      }
    },
    "playground": "#currentMatches"
  },
  {
    "bold": 0,
    "title": "Series Squad List",
    "info": "<b>Coming soon</b><Br><p>The Series squad list API gives you a list of Squads in the given Series. This is yet under development, so please bear with us. Coming soon!</p>"
  },
  {
    "bold": 0,
    "title": "All Players List",
    "info": "<b>A large list of all players in the system</b><Br><p>This API gives you a full list of players with their Country of origin. Based on this you can then query the Player Info API and get more details for each player.</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing the main data of the API",
        "id": "Guid:Unique identifier for this Player",
        "name": "String:Full Name of the player",
        "country": "String:Country the player belongs to"
      }
    },
    "endpoint": "v1/players?apikey=%APIKEY%&offset=0",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": [
        {
          "id": "16592242-ef26-45d9-bf23-fc090e90fbbe",
          "name": "Anderson Phillip",
          "country": "West Indies"
        },
        {
          "id": "9f2abfee-a09f-47c8-a1e5-8eb03fa7b85a",
          "name": "Veerasammy Permaul",
          "country": "West Indies"
        }
      ],
      "status": "success",
      "info": {
        "hitsToday": 7,
        "hitsLimit": 500,
        "credits": 0,
        "server": 18,
        "offsetRows": 0,
        "totalRows": 1992,
        "queryTime": 10.099
      }
    },
    "playground": "#matches"
  },
  {
    "bold": 0,
    "title": "Search All Players",
    "info": "<b>Searches through our entire players database in the system</b><Br><p>This API gives you a full list of players with their Country of origin. Based on this you can then query the Player Info API and get more details for each player.</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing the main data of the API",
        "id": "Guid:Unique identifier for this Player",
        "name": "String:Full Name of the player",
        "country": "String:Country the player belongs to"
      }
    },
    "endpoint": "v1/players?apikey=%APIKEY%&offset=0",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": [
        {
          "id": "16592242-ef26-45d9-bf23-fc090e90fbbe",
          "name": "Anderson Phillip",
          "country": "West Indies"
        },
        {
          "id": "9f2abfee-a09f-47c8-a1e5-8eb03fa7b85a",
          "name": "Veerasammy Permaul",
          "country": "West Indies"
        }
      ],
      "status": "success",
      "info": {
        "hitsToday": 7,
        "hitsLimit": 500,
        "credits": 0,
        "server": 18,
        "offsetRows": 0,
        "totalRows": 1992,
        "queryTime": 10.099
      }
    },
    "playground": "#matches"
  },
  {},
  {
    "bold": 1,
    "title": "Cricket Info APIs",
    "info": "<b>These APIs give you Details of each item shown in the List API</b><Br><p>Details about series, matches, players, etc can be acquired through this API. Keep in mind that this API does NOT have pagination, so if there's a long list or a large API response you will need to handle it accordingly.</p>"
  },
  {
    "bold": 0,
    "title": "Series Info",
    "info": "<b>Detailed info about the Series</b><Br><p>Based on the Series ID provided, this API will give you information about the Series. Beware that the Match List given here is the COMPLETE list, so it will be very HEAVY when the Series has a large number of matches! You should ideally pull this API max 2-3 times a Day or on Manual intervention from your end if required.</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing the main data of the API",
        "info": {
          "~": "The basic details about the Series",
          "id": "Guid:Unique identifier for this Series",
          "name": "String:Name & Year of the Series",
          "startDate": "Date:Start Date & Month of the Series",
          "endDate": "Date:End Date & Month of the Series",
          "odi": "Number:Number of ODIs in this Series",
          "t20": "Number:Number of T20s in this Series",
          "test": "Number:Number of Tests in this Series",
          "squads": "Number:Number of Squads for which data is loaded (series may have more squads for which data is pending / undeclared)",
          "matches": "Number:Number of Matches for which data is loaded (series may have more matches that are pending / undeclared)"
        },
        "matchList": {
          "~": "An array / object containing the Matches in this Series",
          "id": "Guid:Unique identifier for this Match",
          "name": "String:Name of the MAtch",
          "matchType": "String:Type of the match odi,t20,test",
          "status": "String:Latest Match status",
          "venue": "String:Venue of the Match",
          "date": "Date:Date of the Match",
          "dateTimeGMT": "Date:Date and Time of the Match in GMT<Br/>(UTC+00) ISO Format YYYY-MM-DDTHH&#58;mm&#58;ss",
          "teams": "Array:Names of the teams in JSON array",
          "fantasyEnabled": "Boolean:True only if Fantasy Scorecard / Squad / Ball-by-Ball are available for this match"
        }
      }
    },
    "endpoint": "v1/series_info?apikey=%APIKEY%&offset=0&id=47b54677-34de-4378-9019-154e82b9cc1a",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0,
      "id": "47b54677-34de-4378-9019-154e82b9cc1a"
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": {
        "info": {
          "id": "47b54677-34de-4378-9019-154e82b9cc1a",
          "name": "Indian Premier League 2022",
          "startdate": "Mar 26",
          "enddate": "May 29",
          "odi": 0,
          "t20": 70,
          "test": 0,
          "squads": 10,
          "matches": 70
        },
        "matchList": [
          {
            "id": "341e6690-ece0-4dce-83fc-91effbb28eb3",
            "name": "Chennai Super Kings vs Kolkata Knight Riders, 1st Match",
            "matchType": "t20",
            "status": "Match not started",
            "venue": "Wankhede Stadium, Mumbai",
            "date": "2022-03-26",
            "dateTimeGMT": "2022-03-26T14:00:00",
            "teams": [ "Chennai Super Kings", "Kolkata Knight Riders" ],
            "fantasyEnabled": false
          }
        ]
      },
      "status": "success",
      "info": {
        "hitsToday": 12,
        "hitsLimit": 500,
        "credits": 0,
        "server": 11,
        "queryTime": 10
      }
    },
    "playground": "#series_info"
  },
  {
    "bold": 0,
    "title": "Match Info",
    "info": "<b>Detailed info about the Match</b><Br><p>Provides the details of this cricket match. If you require scorecard / ball by ball or other more detailed information, please use the corresponding Fantasy Squad / Fantasy Scorecard / Fantasy Ball-by-Ball API.</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing this Matches detail",
        "id": "Guid:Unique identifier for this Match",
        "name": "String:Name of the Match",
        "matchType": "String:Type of the match odi,t20,test",
        "score": "Object,optional:Score of the match, in inning sequence<Br/><small><b>Contains</b> Team, Inning, Runs, Wickets, Overs</small>",
        "status": "String:Latest Match status",
        "venue": "String:Venue of the Match",
        "date": "Date:Date of the Match",
        "dateTimeGMT": "Date:Date and Time of the Match in GMT<Br/>(UTC+00) ISO Format YYYY-MM-DDTHH&#58;mm&#58;ss",
        "teams": "Array:Names of the teams in JSON array",
        "fantasyEnabled": "Boolean:True only if Fantasy Scorecard / Squad / Ball-by-Ball are available for this match"
      }
    },
    "endpoint": "v1/match_info?apikey=%APIKEY%&offset=0&id=820cfd88-3b56-4a6e-9dd8-1203051140da",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0,
      "id": "820cfd88-3b56-4a6e-9dd8-1203051140da"
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": {
        "id": "2d448290-d882-4e67-9a4a-f62dfea9a51a",
        "name": "Western Australia vs New South Wales, Final",
        "matchType": "odi",
        "status": "Western Australia won by 18 runs",
        "venue": "Junction Oval, Melbourne",
        "date": "2022-03-10",
        "dateTimeGMT": "2022-03-10T23:30:00",
        "teams": [ "Western Australia", "New South Wales" ],
        "score": [
          {
            "r": 207,
            "w": 10,
            "o": 46.3,
            "inning": "Western Australia Inning 1"
          },
          {
            "r": 225,
            "w": 9,
            "o": 50,
            "inning": "New South Wales Inning 1"
          }
        ],
        "tossWinner": "Western Australia",
        "tossChoice": "bat",
        "matchWinner": "Western Australia",
        "series_id": "ff5aa3f3-7164-4766-be90-3b64783257a0",
        "fantasyEnabled": false
      },
      "status": "success",
      "info": {
        "hitsToday": 21,
        "hitsLimit": 500,
        "credits": 0,
        "server": 11,
        "queryTime": 15.7629
      }
    },
    "playground": "#match_info"
  },
  {
    "bold": 0,
    "title": "Player Info",
    "info": "<b>Detailed info about the Player</b><Br><p>Basic details about the player are provided in this API. In future we will include a player photograph (coming soon).</p>",
    "explain": {
      "status": "String:success / failure based on the API result",
      "data": {
        "~": "An array / object containing this Player detail",
        "id": "Guid:Unique identifier for this Player",
        "name": "String:Name of the Player",
        "dateOfBirth": "Date:Date of Birth",
        "role": "String:Player's Role",
        "battingStyle": "String:Batting Style",
        "bowlingStyle": "String:Bowling Style",
        "placeOfBirth": "String:Place of Birth",
        "country": "String:Player's Country"
      }
    },
    "endpoint": "v1/players_info?apikey=%APIKEY%&offset=0&id=16592242-ef26-45d9-bf23-fc090e90fbbe",
    "input": {
      "apikey": "%APIKEY%",
      "offset": 0,
      "id": "16592242-ef26-45d9-bf23-fc090e90fbbe"
    },
    "output": {
      "apikey": "%APIKEY%",
      "data": {
        "id": "16592242-ef26-45d9-bf23-fc090e90fbbe",
        "name": "Anderson Phillip",
        "dateOfBirth": "1996-08-22T00:00:00",
        "role": "Bowler",
        "battingStyle": "Right Handed Bat",
        "bowlingStyle": "Right-arm fast-medium",
        "placeOfBirth": "--",
        "country": "West Indies"
      },
      "status": "success",
      "info": {
        "hitsToday": 41,
        "hitsLimit": 500,
        "credits": 0,
        "server": 11,
        "queryTime": 10
      }
    },
    "playground": "#players_info"
  },
  {},
  {
    "bold": 1,
    "title": "Fantasy API",
    "info": "<span class='badge bg-success'>Work in Progress</span> <b>Detailed Scorecard, Squad and Ball-By-Ball APIs</b><Br><p>Fantasy API includes Scorecard, Ball-by-Ball and Squad API for each match. This is still a work in progress, so expect more changes to come in the future!</p><center><a class='btn btn-lg btn-success' href='/how-to-use-fantasy-cricket-api.aspx'>Get the Fantasy APIs (Scorecard, Squad, Ball-By-Ball, Points, etc) here</a></center>"
  }
];
            x.forEach(renderCodeSlab);
            setTimeout(() => {
                try {
                    document.getElementById(location.hash.replace("#", "")).scrollIntoView()
                    $("BODY").removeClass("loading");
                } catch (e) { }
            }, 50);
        });

        function explainIt(jsoninp) {
            if (!jsoninp) return "";
            if (["string", "number"].includes(typeof jsoninp)) {
                if (("" + jsoninp).includes(":")) {
                    let tags = ("" + jsoninp).split(":")[0];
                    let text = ("" + jsoninp).split(":")[1];
                    return tags.split(",").map(x => {
                        return "<span class='small badge alert-primary'>" + x + "</span>";
                    }).join(' ') + " " + text;
                } else
                    return jsoninp;
            }

            let hmz = "";
            if (jsoninp["~"]) {
                hmz = jsoninp["~"];
                delete jsoninp["~"];
            }

            return hmz + "<table class='table table-striped explainer'>" + Object.keys(jsoninp).map(x => {
                return `<tr><th>` + x + `</th><td>` + explainIt(jsoninp[x]) + `</td></tr>`;
            }).join(' ') + "</table>";
        }

        var baseURL = "https://api.cricapi.com/";

        function renderCodeSlab(x) {
            if (!x.title) {
                // spacer
                $("#sidepan").append("<div>&nbsp;</div>");
                $("#bodyrow").append(`<div class="col-12 mb-5"><hr></div>`);
                return;
            }
            let curID = (++uid);
            let uniqueID = (x.title + "").toLowerCase().replace(/[^A-Za-z0-9]/ig, "-");
            if (curID > 1) $("#APIindex").append("<a class='col-6 col-md-4' href='#api-" + uniqueID + "-" + curID + "'>" + x.title + "</a>");
            $("#sidepan").append("<a href='#api-" + uniqueID + "-" + curID + "'>" + (x.bold ? ("<b>" + x.title + "</b>") : x.title) + "</a>");
            $("#bodyrow").append((`
<div class="col-12 col-md-7 col-lg-8 mb-5"><h2 id='api-${uniqueID + "-" + curID}'>${x.title}</h2>
${x.info}` + ((x.endpoint) ? `<br><input type='text' class='form-control' readonly value='` + baseURL + x.endpoint + `'/>` : "") +
                `<br>${explainIt(x.explain)}</div>
<div class="col-12 col-md-5 col-lg-4 mb-5">`+
                ((x.input) ? `Input<br /><pre class="code">${lineUp(syntaxHighlight(JSON.stringify(x.input, null, 2)))}</pre>` : "") +
                ((x.output) ? `Output<br/><small>(data may be truncated for ease of reading)</small><br /><pre class="code">${lineUp(syntaxHighlight(JSON.stringify(x.output, null, 2)))}</pre>` : "") +
                ((x.playground) ? `<center>Try out the API in real time<br> 
<a href="/member-test.aspx${x.playground}" class='btn btn-sm btn-success'>Code Playground 
<i class='fa fa-arrow-right'></i></a></center></div>`: "")).replaceAll("%APIKEY%", "[your api key]"));
        }



        function lineUp(somey) {
            return "<code>" + somey.split("\n").join("</code><code>") + "</code>";
        }


        function syntaxHighlight(json) {
            json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
                var cls = 'number';
                if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'key';
                    } else {
                        cls = 'string';
                    }
                } else if (/true|false/.test(match)) {
                    cls = 'boolean';
                } else if (/null/.test(match)) {
                    cls = 'null';
                }
                return '<span class="' + cls + '">' + match + '</span>';
            });
        }
    </script>

        </div>
    </div>

    <script>
        // Example starter JavaScript for disabling form submissions if there are invalid fields
        (function () {
            'use strict'

            // Fetch all the forms we want to apply custom Bootstrap validation styles to
            var forms = document.querySelectorAll('.needs-validation')

            // Loop over them and prevent submission
            Array.prototype.slice.call(forms)
                .forEach(function (form) {
                    form.addEventListener('submit', function (event) {
                        if (!form.checkValidity()) {
                            event.preventDefault()
                            event.stopPropagation()
                        }

                        form.classList.add('was-validated')
                    }, false)
                })
        })()

        window._alert = window.alert;
        window._confirm = window.confirm;
        window._prompt = window.prompt;
        window.alert = function (text, title = "Alert") {
            $("#genericModal").modal("show");
            $("#genericModal .modal-body").html(text);
            $("#genericModal .modal-footer *").remove();
            $("#genericModal .modal-footer").html(`<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>`);
            $("#genericModalLabel").html(`<i class="fa fa-info-circle"></i> ` + title);
            $("#genericModal .btn-close").show();
        }
        window.progresswait = function (text) {
            enableWaiting();
            $("#genericModal").modal("show");
            $("#genericModal .modal-body").html(text);
            $("#genericModal .modal-footer *").remove();
            $("#genericModal .modal-footer").html(`<i class='fa fa-spin fa-spinner'></i>`);
            $("#genericModalLabel").html(`<i class="fa fa-info-circle"></i> Please wait`);
            $("#genericModal .btn-close").hide();
        }
        window.progressfinish = function (text) {
            disableWaiting();
            $("#genericModal").modal("hide");
        }
        window.confirm = function (text, yesfn = function () { }, nofn = function () { }) {
            enableWaiting();
            $("#genericModal").modal("show");
            $("#genericModal .modal-body").html(text);
            $("#genericModal .modal-footer *").remove();
            let yesbtn = document.createElement("button");
            yesbtn.className = "btn btn-primary";
            yesbtn.innerHTML = "OK";
            yesbtn.onclick = function () {
                disableWaiting();
                $("#genericModal").modal("hide");
                yesfn();
            }

            let nobtn = document.createElement("button");
            nobtn.className = "btn btn-secondary";
            nobtn.innerHTML = "Cancel";
            nobtn.onclick = function () {
                disableWaiting();
                $("#genericModal").modal("hide");
                nofn();
            }

            $("#genericModal .modal-footer").append(yesbtn);
            $("#genericModal .modal-footer").append(nobtn);
            $("#genericModalLabel").html(`<i class="fa fa-info-circle"></i> Give confirmation`);
            $("#genericModal .btn-close").hide();
        }
        window.prompt = function (text = "Enter the choice", promptResult) {
            enableWaiting();
            $("#genericModal").modal("show");
            $("#genericModal .modal-body").html(text + "<BR><input class='form-control' type='text' id='promptresult' name='promptresult' />");
            $("#genericModal .modal-footer *").remove();
            let yesbtn = document.createElement("button");
            yesbtn.className = "btn btn-primary";
            yesbtn.innerHTML = "OK";
            yesbtn.onclick = function () {
                disableWaiting();
                promptResult($('#promptresult').val());
                $("#genericModal .modal-body").html(" ");
                $("#genericModal").modal("hide");
            }

            let nobtn = document.createElement("button");
            nobtn.className = "btn btn-secondary";
            nobtn.innerHTML = "Cancel";
            nobtn.onclick = function () {
                disableWaiting();
                promptResult(null);
                $("#genericModal .modal-body").html(" ");
                $("#genericModal").modal("hide");
            }

            $("#genericModal .modal-footer").append(yesbtn);
            $("#genericModal .modal-footer").append(nobtn);
            $("#genericModalLabel").html(`<i class="fa fa-info-circle"></i> Give input`);
            $("#genericModal .btn-close").hide();
        }

        window.enableWaiting = function () {
            addEventListener("beforeunload", beforeUnloadListener, { capture: true });
        }
        window.disableWaiting = function () {
            removeEventListener("beforeunload", beforeUnloadListener, { capture: true });
        }
        window.beforeUnloadListener = (event) => {
            event.preventDefault();
            return event.returnValue = "Are you sure you want to exit?";
        };

        window.nicePathHTML = function (pth, endicon = 'fa-folder text-yellow') {
            let result = "";
            let depth = 0;
            if (pth.startsWith('/documents')) {
                result = "<i class='fa fa-hdd text-primary'></i><br>";
                pth = pth.substring(10);
            }
            let arz = pth.trim("/").split("/");

            arz.filter((P) => { return P && (P != ""); })
                .forEach(function (P) {
                    depth++;

                    result += "&nbsp;&nbsp;".repeat(depth) + "<i style='float:none;' class='fa " +
                        ((depth >= (arz.length - 1)) ? endicon : " fa-folder text-yellow  ") +
                        "'></i> " + P + "<br>";
                });

            return result;
        }
    </script>

    <div class="modal fade" id="genericModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-hidden="true" style="background:rgba(0,0,0,0.3);">
        <div class="modal-dialog">
            <div class="modal-content bg-light text-dark">
                <div class="modal-header">
                    <h5 class="modal-title" id="genericModalLabel"><i class="fa fa-info-circle"></i>WoW Berry DMS</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" style="max-height: calc(80vh - 50px); overflow-y: auto; overflow-x:auto;">
                    <p>Check it out!</p>
                    The most powerful Document Management Software ever created.
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
    <!-- TTL 0 ms -->

    <link media="all" onload="this.media='all';" rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">

    <script>
        window.fwSettings = {
            'widget_id': 44000003482
        };
        !function () { if ("function" != typeof window.FreshworksWidget) { var n = function () { n.q.push(arguments) }; n.q = [], window.FreshworksWidget = n } }()
    </script>
<script type="text/javascript" src="https://widget.freshworks.com/widgets/44000003482.js" async="" defer=""></script>

        <!-- Global site tag (gtag.js) - Google Analytics -->
<script async="" defer="" src="https://www.googletagmanager.com/gtag/js?id=G-2VZHSZCDR1"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());

    gtag('config', 'G-2VZHSZCDR1');
</script>
    <script src="https://in-flow.in/scripts/loader.js" data-id="708F98C6A2689B15B5B49C25CA6FADA4261FDE2249B956F515D7A2091EBB9667" data-hint="Click to open"></script>




</body></html>