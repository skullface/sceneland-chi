(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[888],{6840:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/_app",function(){return n(1975)}])},1975:function(e,t,n){"use strict";n.r(t),n.d(t,{default:function(){return _app}});var o=n(5893);n(7375);var a=n(7294),i=n(1163),enqueue=function(e){window.__fathomClientQueue=window.__fathomClientQueue||[],window.__fathomClientQueue.push(e)},flushQueue=function(){window.__fathomClientQueue=window.__fathomClientQueue||[],window.__fathomClientQueue.forEach(function(e){switch(e.type){case"trackPageview":trackPageview(e.opts);return;case"trackGoal":trackGoal(e.code,e.cents);return;case"enableTrackingForMe":enableTrackingForMe();return;case"blockTrackingForMe":blockTrackingForMe();return;case"setSite":setSite(e.id);return}}),window.__fathomClientQueue=[]},checkDomainsAndWarn=function(e){var t=/(https?)(?=:|\/|$)/;e.forEach(function(e){null!==t.exec(e)&&console.warn("The include domain ".concat(e," might fail to work as intended as it begins with a transfer protocol (http://, https://). Consider removing the protocol portion of the string."))})},load=function(e,t){var n=document.createElement("script"),o=document.getElementsByTagName("script")[0]||document.querySelector("body");n.id="fathom-script",n.async=!0,n.setAttribute("data-site",e),n.src=t&&t.url?t.url:"https://cdn.usefathom.com/script.js",t&&(void 0!==t.auto&&n.setAttribute("data-auto","".concat(t.auto)),void 0!==t.honorDNT&&n.setAttribute("data-honor-dnt","".concat(t.honorDNT)),void 0!==t.canonical&&n.setAttribute("data-canonical","".concat(t.canonical)),t.includedDomains&&(checkDomainsAndWarn(t.includedDomains),n.setAttribute("data-included-domains",t.includedDomains.join(","))),t.excludedDomains&&(checkDomainsAndWarn(t.excludedDomains),n.setAttribute("data-excluded-domains",t.excludedDomains.join(","))),t.spa&&n.setAttribute("data-spa",t.spa)),n.onload=flushQueue,o.parentNode.insertBefore(n,o)},trackPageview=function(e){window.fathom?e?window.fathom.trackPageview(e):window.fathom.trackPageview():enqueue({type:"trackPageview",opts:e})},trackGoal=function(e,t){window.fathom?window.fathom.trackGoal(e,t):enqueue({type:"trackGoal",code:e,cents:t})},blockTrackingForMe=function(){window.fathom?window.fathom.blockTrackingForMe():enqueue({type:"blockTrackingForMe"})},enableTrackingForMe=function(){window.fathom?window.fathom.enableTrackingForMe():enqueue({type:"enableTrackingForMe"})},setSite=function(e){window.fathom?window.fathom.setSite(e):enqueue({type:"setSite",id:e})},_app=e=>{let{Component:t,pageProps:n}=e,c=(0,i.useRouter)();return(0,a.useEffect)(()=>{function onRouteChangeComplete(){trackPageview()}return load("VUYLHUEU",{includedDomains:["312.show"]}),c.events.on("routeChangeComplete",onRouteChangeComplete),()=>{c.events.off("routeChangeComplete",onRouteChangeComplete)}},[c.events]),(0,o.jsx)(t,{...n})}},7375:function(){},1163:function(e,t,n){e.exports=n(8355)}},function(e){var __webpack_exec__=function(t){return e(e.s=t)};e.O(0,[774,179],function(){return __webpack_exec__(6840),__webpack_exec__(8355)}),_N_E=e.O()}]);