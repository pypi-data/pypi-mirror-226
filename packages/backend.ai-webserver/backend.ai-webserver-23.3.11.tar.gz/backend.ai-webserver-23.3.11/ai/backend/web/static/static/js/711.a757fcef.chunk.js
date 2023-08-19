"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[711],{1502:function(n,e,t){t.r(e),t.d(e,{default:function(){return P},useShadowRoot:function(){return T},useWebComponentInfo:function(){return V}});var i=t(9439),r=t(4519),a=t(6980),o=t(7340),l=t(9002),u=t(7112),s=t(4447),c=t(1748),d=t(3881),g=t(9883),v=t(6670),f=t(4165),h=t(5861),m=t(1011),b=t(1413);function p(n,e){var t=(0,b.Z)({},e);return function(n){for(var e,t=/(\w+)\s@\s*(\w+)\s*\(\s*(\w+)\s*:\s*(\$?\w+)\s*\)/g,r=[];null!==(e=t.exec(n));){var a=e,o=(0,i.Z)(a,5),l=o[0],u=o[1],s=o[2],c=o[3],d=o[4];r.push({fieldName:u,directive:s,argumentName:c,argumentValue:d,originFieldStr:l})}return r}(n).forEach((function(i){if("skipOnClient"===i.directive&&"if"===i.argumentName&&(n=!i.argumentValue||!0!==e[i.argumentValue.substring(1)]&&"true"!==i.argumentValue?n.replace(i.originFieldStr,i.originFieldStr.replace(/@\s*(skipOnClient)\s*\(\s*(\w+)\s*:\s*(\$?\w+)\s*\)/,"")):n.replace(i.originFieldStr,""),i.argumentValue.startsWith("$")&&2===n.split(i.argumentValue).length)){var r=i.argumentValue.substring(1),a=new RegExp(".*".concat(r,".*\n"),"g");n=n.replace(a,""),delete t[i.argumentValue.substring(1)]}})),{query:n,variables:t}}m.RelayFeatureFlags.ENABLE_RELAY_RESOLVERS=!0;var w=function(){var n=(0,h.Z)((0,f.Z)().mark((function n(e,t){var i,r,a,o,l,u;return(0,f.Z)().wrap((function(n){for(;;)switch(n.prev=n.next){case 0:return a=p(e.text||"",t),o={query:a.query,variables:a.variables},l=null===(i=globalThis.backendaiclient)||void 0===i?void 0:i.newSignedRequest("POST","/admin/gql",o),n.next=5,null===(r=globalThis.backendaiclient)||void 0===r?void 0:r._wrapWithPromise(l,!1,null,1e4,0);case 5:return u=n.sent,n.abrupt("return",u);case 7:case"end":return n.stop()}}),n)})));return function(e,t){return n.apply(this,arguments)}}();var k,x=new m.Environment({network:m.Network.create(w,void 0),store:new m.Store(new m.RecordSource)}),y=t(382),C=t(1843),E=t(2674),S=t(2556),j=r.createContext(null),L=r.createContext(null),T=function(){return r.useContext(L)},V=function(){return r.useContext(j)},Z=new u.QueryClient({defaultOptions:{queries:{suspense:!0,refetchOnWindowFocus:!1,retry:!1}}});s.ZP.use(c.Db).use(d.Z).init({backend:{loadPath:"/resources/i18n/{{lng}}.json"},lng:(null===globalThis||void 0===globalThis||null===(k=globalThis.backendaioptions)||void 0===k?void 0:k.get("current_language"))||"en",fallbackLng:"en",interpolation:{escapeValue:!1}});var _=function(){var n=(0,E.s0)();return(0,r.useLayoutEffect)((function(){var e=function(e){var t=e.detail;n(t,{replace:!0})};return document.addEventListener("react-navigate",e),function(){document.removeEventListener("react-navigate",e)}}),[n]),null},P=function(n){var e=n.children,t=n.value,s=n.styles,d=n.shadowRoot,f=n.dispatchEvent,h=(0,r.useMemo)((function(){return(0,o.Df)()}),[]),m=function(){var n,e=(0,r.useState)(null===globalThis||void 0===globalThis||null===(n=globalThis.backendaioptions)||void 0===n?void 0:n.get("current_language")),t=(0,i.Z)(e,2),a=t[0],o=t[1],l=(0,c.$G)().i18n;return(0,r.useEffect)((function(){setTimeout((function(){return null===l||void 0===l?void 0:l.changeLanguage(a)}),0)}),[]),(0,r.useEffect)((function(){var n=function(n){var e,t;o(null===n||void 0===n||null===(e=n.detail)||void 0===e?void 0:e.lang);var i=(null===n||void 0===n||null===(t=n.detail)||void 0===t?void 0:t.lang)||"en";null===l||void 0===l||l.changeLanguage(i)};return window.addEventListener("langChanged",n),function(){return window.removeEventListener("langChanged",n)}}),[l]),[a]}(),b=(0,i.Z)(m,1)[0],p=(0,y.x)(),w=(0,r.useMemo)((function(){return{value:t,dispatchEvent:f,moveTo:function(n){f("moveTo",{path:n})}}}),[t,f]);return(0,S.jsx)(S.Fragment,{children:x&&(0,S.jsx)(a.RelayEnvironmentProvider,{environment:x,children:(0,S.jsxs)(r.StrictMode,{children:[(0,S.jsxs)("style",{children:[s,"\n.anticon {\n  display: inline-block;\n  color: inherit;\n  font-style: normal;\n  line-height: 0;\n  text-align: center;\n  text-transform: none;\n  vertical-align: -0.125em;\n  text-rendering: optimizeLegibility;\n  -webkit-font-smoothing: antialiased;\n  -moz-osx-font-smoothing: grayscale;\n}\n\n.anticon > * {\n  line-height: 1;\n}\n\n.anticon svg {\n  display: inline-block;\n}\n\n.anticon::before {\n  display: none;\n}\n\n.anticon .anticon-icon {\n  display: block;\n}\n\n.anticon[tabindex] {\n  cursor: pointer;\n}\n\n.anticon-spin::before,\n.anticon-spin {\n  display: inline-block;\n  -webkit-animation: loadingCircle 1s infinite linear;\n  animation: loadingCircle 1s infinite linear;\n}\n\n@-webkit-keyframes loadingCircle {\n  100% {\n    -webkit-transform: rotate(360deg);\n    transform: rotate(360deg);\n  }\n}\n\n@keyframes loadingCircle {\n  100% {\n    -webkit-transform: rotate(360deg);\n    transform: rotate(360deg);\n  }\n}\n"]}),(0,S.jsx)(u.QueryClientProvider,{client:Z,children:(0,S.jsx)(L.Provider,{value:d,children:(0,S.jsx)(j.Provider,{value:w,children:(0,S.jsx)(l.ZP,{getPopupContainer:function(n){return d},locale:"ko"===b?v.Z:g.Z,theme:p,children:(0,S.jsx)(o.V9,{container:d,cache:h,children:(0,S.jsx)(r.Suspense,{fallback:"",children:(0,S.jsxs)(C.VK,{children:[(0,S.jsx)(_,{}),e]})})})})})})})]})})})}}}]);
//# sourceMappingURL=711.a757fcef.chunk.js.map