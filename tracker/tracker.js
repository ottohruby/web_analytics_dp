// initialize only once
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
        device_id = undefined,
        session_id = undefined,
        campaign_data = undefined,
        device_type = undefined,
        new_device = undefined,
        new_session = undefined,
        tracking_url = undefined;

    /*
        Private methods
    */

    function getCookie(name) {
        var name = name + "=";
        var cookie_str = decodeURIComponent(document.cookie);
        var cookies = cookie_str.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.indexOf(name) === 0) {
                return cookie.substring(name.length, cookie.length);
            }
        }
        return undefined;
    }

    function setCookie(name,value,days) {
        var expires = "";
        if (days) {
            var date = new Date();
            date.setTime(date.getTime() + (days*24*60*60*1000));
            expires = "; expires=" + date.toUTCString();
        }
        document.cookie = name + "=" + (value || "")  + expires + "; path=/";
    }

    function getSessionId(){
        return session_id || getCookie('_tDP_sid') || generateSessionId();
    }

    function generateCampaignData(){
        campaign_data = {'s': '(direct)', 'm': '(none)', 'c': '(direct)'};
        setCookie('_tDP_cmp', JSON.stringify(campaign_data));
        return campaign_data;
    }

    function getCampaignData(){
        return campaign_data || JSON.parse(getCookie('_tDP_cmp')) || generateCampaignData();
    }

    function generateSessionId(){
        session_id = currentTimestampMillis();
        new_session = true;
        setCookie('_tDP_sid', session_id);
        return session_id;
    }

    function getDeviceId(){
        return device_id || getCookie('_tDP_did') || generateDeviceId();
    }
    
    function generateDeviceId(){
        device_id = randomInt(1000000000, 9999999999) + '.' + getSessionId();
        new_device = true;
        setCookie('_tDP_did', device_id, 100);
        return device_id;
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

    function getDeviceType(){
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

    function sendXmlHttpRequest(request) {
        try {
            console.log(tracking_url, 'url');
            var xhr = new window_alias.XMLHttpRequest();
            xhr.open('POST', 'https://dp-logger.ottohruby.cz/events/collect/v1', true);
    
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
        this.lg_id = 0;
        this.aw_id = 0;
    }

    /*
        Public methods
    */

    Tracker.prototype.enable = function(tracking_url, lg_id=0, aw_id=0){
        if(this.enabled){ return true; }
        this.enabled = true;
        this.lg_id = lg_id;
        this.aw_id = aw_id;
        tracking_url = 'https://dp-logger.ottohruby.cz/events/collect/v1'; // todo
        getDeviceId();
        getSessionId();
        // get_campaign_data
        if(new_device){ this.push(0); }
        if(new_session){ this.push(1); }
        this.push(2); // page_view
        return true;
    };

    Tracker.prototype.push = function(en_id, dims, metrics){
        console.log('push');
        // if(!this.enabled) { return; }
        if(en_id==undefined){ return; }

        var data = {};
        //add common data
        data.lg_id = this.lg_id;
        data.aw_id = this.aw_id;
        data.ev_ts = new Date().toISOString();
        data.en_id = en_id;
        
        data.dims = dims || {};
        // add device_id, page_domain, page_path, session_id
        data.dims["0"] = {"val": getDeviceId()};
        data.dims["1"] = {"val": getDeviceType()};
        data.dims["2"] = {"val": getPageDomain()};
        data.dims["3"] = {"val": getPagePath()};
        data.dims["4"] = {"val": getPageTitle()};
        data.dims["5"] = {"val": getPageReferrer()};
        data.dims["6"] = {"val": getSessionId()};
        var cmp_data = getCampaignData();
        data.dims["7"] = cmp_data.s;
        data.dims["8"] = cmp_data.m
        data.dims["9"] = cmp_data.c;
        
        data.metrics = metrics || {};
        // add event_count if missing
        data.metrics["0"] = data.metrics["0"] || {"val": 1, "unit": 0};         
        console.log(data, 'data')
        sendData(data);
    }

    window.TrackerDP = new Tracker();
    })()
}