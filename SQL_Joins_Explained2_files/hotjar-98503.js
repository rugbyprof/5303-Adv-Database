window.hjSiteSettings = window.hjSiteSettings || {"testers_widgets":[],"surveys":[],"record_targeting_rules":[],"recording_capture_keystrokes":true,"polls":[],"site_id":98503,"forms":[],"record":false,"heatmaps":[],"deferred_page_contents":[],"feedback_widgets":[],"r":1.0};

window.hjBootstrap = window.hjBootstrap || function (scriptUrl) {
    var s = document.createElement('script');
    s.src = scriptUrl;
    document.getElementsByTagName('head')[0].appendChild(s);
    window.hjBootstrap = function() {};
};

hjBootstrap('https://script.hotjar.com/modules-b8f33ddee80c6a690b3be20ca1f14dd4.js');