"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[505,502],{1502:function(n,e,t){t.r(e),t.d(e,{default:function(){return _},useShadowRoot:function(){return j},useWebComponentInfo:function(){return E}});var i=t(9439),r=t(4519),a=t(6980),o=t(6114),l=t(9002),u=t(7112),c=t(4447),s=t(1748),d=t(3881),f=t(9883),g=t(6670),v=t(4165),h=t(5861),p=t(1011),b=t(1413);function m(n,e){var t=(0,b.Z)({},e);return function(n){for(var e,t=/(\w+)\s@\s*(\w+)\s*\(\s*(\w+)\s*:\s*(\$?\w+)\s*\)/g,r=[];null!==(e=t.exec(n));){var a=e,o=(0,i.Z)(a,5),l=o[0],u=o[1],c=o[2],s=o[3],d=o[4];r.push({fieldName:u,directive:c,argumentName:s,argumentValue:d,originFieldStr:l})}return r}(n).forEach((function(i){if("skipOnClient"===i.directive&&"if"===i.argumentName&&(n=!i.argumentValue||!0!==e[i.argumentValue.substring(1)]&&"true"!==i.argumentValue?n.replace(i.originFieldStr,i.originFieldStr.replace(/@\s*(skipOnClient)\s*\(\s*(\w+)\s*:\s*(\$?\w+)\s*\)/,"")):n.replace(i.originFieldStr,""),i.argumentValue.startsWith("$")&&2===n.split(i.argumentValue).length)){var r=i.argumentValue.substring(1),a=new RegExp(".*".concat(r,".*\n"),"g");n=n.replace(a,""),delete t[i.argumentValue.substring(1)]}})),{query:n,variables:t}}p.RelayFeatureFlags.ENABLE_RELAY_RESOLVERS=!0;var w=function(){var n=(0,h.Z)((0,v.Z)().mark((function n(e,t){var i,r,a,o,l,u;return(0,v.Z)().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return a=m(e.text||"",t),o={query:a.query,variables:a.variables},l=null===(i=globalThis.backendaiclient)||void 0===i?void 0:i.newSignedRequest("POST","/admin/gql",o),n.next=5,null===(r=globalThis.backendaiclient)||void 0===r?void 0:r._wrapWithPromise(l,!1,null,1e4,0);case 5:return u=n.sent,n.abrupt("return",u);case 7:case"end":return n.stop()}}),n)})));return function(e,t){return n.apply(this,arguments)}}();var k,x=new p.Environment({network:p.Network.create(w,void 0),store:new p.Store(new p.RecordSource)}),y=t(382),S=t(4322),C=t(2556),T=r.createContext(null),Z=r.createContext(null),j=function(){return r.useContext(Z)},E=function(){return r.useContext(T)},M=new u.QueryClient({defaultOptions:{queries:{suspense:!0,refetchOnWindowFocus:!1,retry:!1}}});c.ZP.use(s.Db).use(d.Z).init({backend:{loadPath:"/resources/i18n/{{lng}}.json"},lng:(null===globalThis||void 0===globalThis||null===(k=globalThis.backendaioptions)||void 0===k?void 0:k.get("current_language"))||"en",fallbackLng:"en",interpolation:{escapeValue:!1}});var _=function(n){var e=n.children,t=n.value,c=n.styles,d=n.shadowRoot,v=n.dispatchEvent,h=(0,r.useMemo)((function(){return(0,o.Df)()}),[]),p=function(){var n,e=(0,r.useState)(null===globalThis||void 0===globalThis||null===(n=globalThis.backendaioptions)||void 0===n?void 0:n.get("current_language")),t=(0,i.Z)(e,2),a=t[0],o=t[1],l=(0,s.$G)().i18n;return(0,r.useEffect)((function(){setTimeout((function(){return null===l||void 0===l?void 0:l.changeLanguage(a)}),0)}),[]),(0,r.useEffect)((function(){var n=function(n){var e,t;o(null===n||void 0===n||null===(e=n.detail)||void 0===e?void 0:e.lang);var i=(null===n||void 0===n||null===(t=n.detail)||void 0===t?void 0:t.lang)||"en";null===l||void 0===l||l.changeLanguage(i)};return window.addEventListener("langChanged",n),function(){return window.removeEventListener("langChanged",n)}}),[l]),[a]}(),b=(0,i.Z)(p,1)[0],m=(0,y.x)(),w=(0,r.useMemo)((function(){return{value:t,dispatchEvent:v,moveTo:function(n){v("moveTo",{path:n})}}}),[t,v]);return(0,C.jsx)(C.Fragment,{children:x&&(0,C.jsx)(a.RelayEnvironmentProvider,{environment:x,children:(0,C.jsxs)(r.StrictMode,{children:[(0,C.jsxs)("style",{children:[c,"\n.anticon {\n  display: inline-block;\n  color: inherit;\n  font-style: normal;\n  line-height: 0;\n  text-align: center;\n  text-transform: none;\n  vertical-align: -0.125em;\n  text-rendering: optimizeLegibility;\n  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale;\n}\n\n.anticon > * {\n  line-height: 1;\n}\n\n.anticon svg {\n  display: inline-block;\n}\n\n.anticon::before {\n  display: none;\n}\n\n.anticon .anticon-icon {\n  display: block;\n}\n\n.anticon[tabindex] {\n  cursor: pointer;\n}\n\n.anticon-spin::before,\n.anticon-spin {\n  display: inline-block;\n  -webkit-animation: loadingCircle 1s infinite linear;\n  animation: loadingCircle 1s infinite linear;\n}\n\n@-webkit-keyframes loadingCircle {\n  100% {\n    -webkit-transform: rotate(360deg);\n    transform: rotate(360deg);\n  }\n}\n\n@keyframes loadingCircle {\n  100% {\n    -webkit-transform: rotate(360deg);\n    transform: rotate(360deg);\n  }\n}\n"]}),(0,C.jsx)(u.QueryClientProvider,{client:M,children:(0,C.jsx)(Z.Provider,{value:d,children:(0,C.jsx)(T.Provider,{value:w,children:(0,C.jsx)(l.ZP,{getPopupContainer:function(n){return null!==n&&void 0!==n&&n.parentNode?n.parentNode:d},locale:"ko"===b?g.Z:f.Z,theme:m,children:(0,C.jsx)(o.V9,{container:d,cache:h,children:(0,C.jsx)(r.Suspense,{fallback:"",children:(0,C.jsx)(S.VK,{children:e})})})})})})})]})})})}},9277:function(n,e,t){var i=t(1413),r=t(4925),a=t(4036),o=(t(4519),t(2556)),l=["direction","wrap","justify","align","gap","style","children"];e.Z=function(n){var e=n.direction,t=void 0===e?"row":e,u=n.wrap,c=void 0===u?"nowrap":u,s=n.justify,d=void 0===s?"flex-start":s,f=n.align,g=void 0===f?"center":f,v=n.gap,h=void 0===v?0:v,p=n.style,b=n.children,m=(0,r.Z)(n,l),w=a.Z.useToken().token,k=[d,g],x=null===k||void 0===k?void 0:k.map((function(n){var e;switch(n){case"start":e="flex-start";break;case"end":e="flex-end";break;case"between":e="space-between";break;case"around":e="space-around";break;default:e=n}return e})),y=(0,i.Z)({display:"flex",flexDirection:t,flexWrap:c,justifyContent:x[0],alignItems:x[1]},p);return(0,o.jsx)("div",(0,i.Z)((0,i.Z)({style:(0,i.Z)({alignItems:"stretch",backgroundColor:"transparent",border:"0 solid black",boxSizing:"border-box",display:"flex",flexBasis:"auto",flexDirection:"column",flexShrink:0,listStyle:"none",margin:0,minHeight:0,minWidth:0,padding:0,position:"relative",textDecoration:"none",gap:"string"===typeof h?w["padding"+h.toUpperCase()]:h},y)},m),{},{children:b}))}},3255:function(n,e,t){t.d(e,{Hz:function(){return l},Lc:function(){return a},Uz:function(){return u},VQ:function(){return c},We:function(){return r},en:function(){return o}});var i=t(2556),r=function(n){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:/(<br\s*\/?>|\n)/;return n.split(e).map((function(n,t){return n.match(e)?(0,i.jsx)("br",{},t):n}))},a=function(n){var e=n.method,t=n.url,i=n.body,r=void 0===i?null:i,a=n.client,o=null===a||void 0===a?void 0:a.newSignedRequest(e,t,r,null);return null===a||void 0===a?void 0:a._wrapWithPromise(o)},o=function(){var n=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2;if(0===n)return"0 Bytes";var t=Math.pow(10,3);e=e<0?0:e;var i=Math.floor(Math.log(Math.round(n))/Math.log(t));return i=i<0?0:i,parseFloat((n/Math.pow(t,i)).toFixed(e))+" "+["Bytes","KB","MB","GB","TB","PB"][i]},l=function(){var n=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,e=Math.pow(10,9);return Math.round(e*n)},u=function(n){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2;return null===n||void 0===n?arguments.length>2&&void 0!==arguments[2]?arguments[2]:"-":n?(n/Math.pow(10,9)).toFixed(e):n},c=function(n,e){return""===e||void 0===e?"":e.startsWith("".concat(n,":"))?e:"".concat(n,":").concat(e)}},7760:function(n,e,t){t.d(e,{Dj:function(){return c},Kr:function(){return o},M:function(){return u},tQ:function(){return l}});var i=t(9439),r=t(4519),a=t(7112),o=function(n){var e=(0,r.useState)(n||(new Date).toISOString()),t=(0,i.Z)(e,2),a=t[0],o=t[1];return[a,function(n){o(n||(new Date).toISOString())}]},l=function(){return c()._config.domainName},u=function(n){var e=n.api_endpoint;return(0,r.useMemo)((function(){var n=new globalThis.BackendAIClientConfig("","",e,"SESSION");return new globalThis.BackendAIClient(n,"Backend.AI Console.")}),[e])},c=function(){return(0,a.useQuery)({queryKey:"backendai-client-for-suspense",queryFn:function(){return new Promise((function(n){if("undefined"!==typeof globalThis.backendaiclient&&null!==globalThis.backendaiclient&&!1!==globalThis.backendaiclient.ready)return n(globalThis.backendaiclient);document.addEventListener("backend-ai-connected",(function e(){n(globalThis.backendaiclient),document.removeEventListener("backend-ai-connected",e)}))}))},retry:!1,suspense:!0}).data}}}]);
//# sourceMappingURL=505.51098dee.chunk.js.map