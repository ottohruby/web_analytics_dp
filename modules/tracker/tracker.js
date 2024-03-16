
        if (typeof window.TrackerDP !== 'object') {
            (function () {
            /*
                Private variables
            */
            // aliases for minification
            var
                document_alias = document,
                window_alias = window;
            
            // internal vars
            var
                visitor_id = undefined,
                session_id = undefined,
                campaign_data = undefined,
                device_type = undefined,
                new_visitor = undefined,
                new_session = undefined,
                session_data = undefined,
                tracking_url = undefined;
        
            /*
                Private methods
            */
        
            function getCookie(name) {
                name = name + "=";
                var cookie_str = decodeURIComponent(document.cookie);
                var cookies = cookie_str.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    if (cookie.indexOf(name) === 0) {
                        return cookie.substring(name.length, cookie.length);
                    }
                }
                return undefined;
            }
        
            function setCookie(name,value,minutes) {
                var expires = "";
                if (minutes) {
                    var date = new Date();
                    date.setTime(date.getTime() + (minutes*60*1000));
                    expires = "; expires=" + date.toUTCString();
                }
                document.cookie = name + "=" + (value || "")  + expires + "; path=/";
            }
        
            function hostnameFromUrl(url){
                var l = document.createElement("a");
                l.href = url;
                return l.hostname;
            }
        
            function generateCampaignData(){
                var params = (new URL(window_alias.document.location)).searchParams;
                var utm_source = params.get("utm_source");
                var utm_medium = params.get("utm_medium");
                var utm_campaign = params.get("utm_campaign");
                if(utm_source || utm_medium || utm_campaign){
                    return {'s': utm_source, 'm': utm_medium || "(manual)", 'c': utm_campaign || "(manual)"};
                }
        
                var referrer = getPageReferrer();
                if(referrer == ''){
                    return {'s': 'direct', 'm': '(none)', 'c': '(none)'};    
                }
        
                var search_engines = {
                    "(http(s)?:\/\/|www\.)(search\.)?google\.": "google",
                    "search\.seznam\.": "seznam",
                    "(http(s)?:\/\/|www\.)(search\.)?bing\.": "bing",
                    "search(atlas)?\.centrum\.": "centrum",
                    "search\.yahoo\.": "yahoo",
                    "duckduckgo\.": "duckduckgo"
                };
        
                for (var engine in search_engines) {
                    var regex = new RegExp(engine);
                    if (regex.test(referrer)) {
                      return {'s': search_engines[engine], 'm': 'organic', 'c': '(organic)'};
                    }
                }
                
                if (!referrer.includes(getPageDomain())) {
                    return {'s': hostnameFromUrl(referrer), 'm': 'referral', 'c': '(referral)'};
                }
                return {'s': 'direct', 'm': '(none)', 'c': '(none)'};
            }
        
            function generateSessionData(){
                var s = getCookie('_tDP_sess');
                var session_data = {};
                if(s){
                    session_data = JSON.parse(s) || {};
                    session_data.sid = session_data.sid;
                    session_data.cmp = session_data.cmp;
                }
                if(session_data.sid == undefined) {
                    session_data.sid = currentTimestampMillis();
                    new_session = true;
                    session_data.cmp = generateCampaignData();
                }
        
                setCookie('_tDP_sess', JSON.stringify(session_data), 30);
                return session_data;
            }
        
            function getSessionId(){
                return session_id || getSessionData().sid;
            }
        
            function getSessionData(){
                var session_data = session_data || generateSessionData() || {};
                session_id = session_data.sid;
                campaign_data = session_data.cmp;
                return session_data;
            }
        
            function generateVisitorId(){
                var c = getCookie('_tDP_vid');
                if(c){
                    visitor_id = c;
                }
                if(visitor_id==undefined){
                    visitor_id = randomInt(1000000000, 9999999999) + '.' + getSessionId();
                    new_visitor = true;
                }
                setCookie('_tDP_vid', visitor_id, 100*60*24);
                return visitor_id;
            }

            function initClickTracking(){
                function handleClick(event) {
                    var clickedElement = event.target;
    
                    if ((clickedElement.tagName === 'A') || (clickedElement.tagName === 'BUTTON')) {
                        if (clickedElement.tagName === 'A') {
                            var linkText = clickedElement.innerText;
                            var dims = {"11": {"val": clickedElement.getAttribute('href')}};
                            window_alias.TrackerDP.push(5, dims, undefined);
                        } 
                    }
                }
                document.addEventListener('click', handleClick);
            }

            function initScrollTracking(){
                var scroll_50 = false;
                var scroll_75 = false;
                function checkScroll() {
                    if((scroll_75 == false) || (scroll_50 == false)){
                        var percent = getVerticalScrollPercent();
                        if((percent >= 75) && (scroll_75 == false)){
                            scroll_75 = true;
                            var metrics= {"5": {"val": 75, "unit": 2}};
                            window_alias.TrackerDP.push(4, undefined, metrics);
                        }
                        if((percent >= 50) && (scroll_50 == false)){
                            scroll_50 = true;
                            var metrics= {"5": {"val": 50, "unit": 2}};
                            window_alias.TrackerDP.push(4, undefined, metrics);
                        }
                    }
                };

                setInterval(checkScroll, 100);
            }

            function getVerticalScrollPercent() {
                var h = document.documentElement;
                var b = document.body;
                var st = 'scrollTop';
                var sh = 'scrollHeight';
                return (h[st]||b[st]) / ((h[sh]||b[sh]) - h.clientHeight) * 100;
            }
        
            function getVisitorId(){
                return visitor_id || generateVisitorId();
            }
            
            function currentTimestampMillis(){
                return Date.now();
            }
        
            function randomInt(min, max) {
                return Math.floor(Math.random() * (max - min + 1)) + min;
            }
        
            function getPageDomain(){
                return window_alias.location.hostname.replace('www.','');
            }
            
            function getPagePath(){
                return window_alias.location.pathname;
            }
            
            function getPageTitle(){
                return window_alias.document.title;
            }
        
            function getPageReferrer(){
                return window_alias.document.referrer;
            }
        
            function generateDeviceType(){
                var ua = window_alias.navigator.userAgent.toLowerCase();
                if(ua.indexOf("iphone") > -1){ return "phone"; }
                if(ua.indexOf("ipad") > -1){ return "tablet"; }
                if(ua.indexOf("mac") > -1){ return "desktop"; }
                if(ua.indexOf("mobi") > -1){ return "phone"; }
                if(ua.indexOf("android") > -1){ return "tablet"; }
        
                if (navigator.maxTouchPoints == 0){
                    return 'desktop';
                }
                if (window.matchMedia('only screen and (any-pointer: fine)').matches) {
                    return 'desktop';
                }
                if(window.matchMedia('(orientation: portrait) and (min-device-height: 768px)').matches){
                    return 'tablet';
                }
                if(window.matchMedia('(orientation: portrait)').matches){
                    return 'tablet';
                }
                if(window.matchMedia('(orientation: landscape) and (min-device-width: 768px)').matches){
                    return 'phone';
                }
                if(window.matchMedia('(orientation: landscape)').matches){
                    return 'phone';
                }
                return "n/a";
            }
        
            function getDeviceType(){
                if(!device_type){
                    device_type = generateDeviceType();
                }
                return device_type;
            }
        
            function transformDimsToArr(dims) {     
                var transformed_dims = [];
                
                for (var key in dims) {
                  if (dims.hasOwnProperty(key)) {
                    var obj = {
                      id: parseInt(key),
                      val: (dims[key] || {}).val
                    };
                    transformed_dims.push(obj);
                  }
                }
            
                return transformed_dims;
            }      
        
            function transformMetricsToArr(metrics) {     
                var transformed_metrics = [];
                
                for (var key in metrics) {
                  if (metrics.hasOwnProperty(key)) {
                    var obj = {
                      id: parseInt(key),
                      val: (metrics[key] || {}).val,
                      unit: parseInt((metrics[key] || {}).unit)
                    };
                    transformed_metrics.push(obj);
                  }
                }
                return transformed_metrics;
            }      
        
            function sendData(data){
                data.dims = transformDimsToArr(data.dims);
                data.metrics = transformMetricsToArr(data.metrics);
                sendXmlHttpRequest(data);
            }
        
            function setTrackingUrl(url){
                tracking_url = url;
            }
        
            function sendXmlHttpRequest(request) {
                try {
                    var xhr = new window_alias.XMLHttpRequest();
                    xhr.open('POST', tracking_url, true);
            
                    xhr.setRequestHeader('Content-Type', 'application/json');
                    // xhr.withCredentials = true;
                    xhr.send(JSON.stringify(request));
                } catch (e) {
            
                }
            }
        
            function Tracker() {
                /*
                    Public variables
                */
                this.enabled = false;
                this.lg_id = 1;
                this.aw_id = 1;
            }
        
            /*
                Public methods
            */
        
            Tracker.prototype.enable = function(tracking_url, lg_id, aw_id){
                tracking_url = tracking_url || 'https://dp-logger.ottohruby.cz/events/collect/v1';
                lg_id = lg_id || 1;
                aw_id = aw_id || 1;
                if(this.enabled){ return true; }
                this.enabled = true;
                this.lg_id = lg_id;
                this.aw_id = aw_id;
                setTrackingUrl(tracking_url);
                getVisitorId();
                getSessionData();
                if(new_visitor){ this.push(1); }
                if(new_session){ this.push(2); }
                initScrollTracking();
                initClickTracking();
                this.push(3); // page_view
                return true;
            };
        
            Tracker.prototype.push = function(en_id, dims, metrics){
                if(!this.enabled) { return; }
                if(en_id==undefined){ return; }
        
                var data = {};
                //add common data
                data.lg_id = this.lg_id;
                data.aw_id = this.aw_id;
                data.ev_ts = new Date().toISOString();
                data.en_id = en_id;
                
                data.dims = dims || {};
                // add visitor_id, page_domain, page_path, session_id
                data.dims["1"] = {"val": getVisitorId()};
                data.dims["2"] = {"val": getDeviceType()};
                data.dims["3"] = {"val": getPageDomain()};
                data.dims["4"] = {"val": getPagePath()};
                data.dims["5"] = {"val": getPageTitle()};
                data.dims["6"] = {"val": getPageReferrer()};
                data.dims["7"] = {"val": getSessionId()};
                data.dims["8"] = {"val": campaign_data.s};
                data.dims["9"] = {"val": campaign_data.m};
                data.dims["10"] = {"val": campaign_data.c};
                
                data.metrics = metrics || {};
                data.metrics["1"] = data.metrics["1"] || {"val": 1, "unit": 1};         
                sendData(data);
            }
        
            window.TrackerDP = new Tracker();
            })()
        }
