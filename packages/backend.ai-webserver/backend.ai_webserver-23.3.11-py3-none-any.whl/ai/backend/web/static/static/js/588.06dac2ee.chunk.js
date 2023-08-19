"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[588],{1662:function(e,t,n){n.d(t,{Z:function(){return u}});var r=n(7462),o=n(4519),c={icon:{tag:"svg",attrs:{"fill-rule":"evenodd",viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M799.86 166.31c.02 0 .04.02.08.06l57.69 57.7c.04.03.05.05.06.08a.12.12 0 010 .06c0 .03-.02.05-.06.09L569.93 512l287.7 287.7c.04.04.05.06.06.09a.12.12 0 010 .07c0 .02-.02.04-.06.08l-57.7 57.69c-.03.04-.05.05-.07.06a.12.12 0 01-.07 0c-.03 0-.05-.02-.09-.06L512 569.93l-287.7 287.7c-.04.04-.06.05-.09.06a.12.12 0 01-.07 0c-.02 0-.04-.02-.08-.06l-57.69-57.7c-.04-.03-.05-.05-.06-.07a.12.12 0 010-.07c0-.03.02-.05.06-.09L454.07 512l-287.7-287.7c-.04-.04-.05-.06-.06-.09a.12.12 0 010-.07c0-.02.02-.04.06-.08l57.7-57.69c.03-.04.05-.05.07-.06a.12.12 0 01.07 0c.03 0 .05.02.09.06L512 454.07l287.7-287.7c.04-.04.06-.05.09-.06a.12.12 0 01.07 0z"}}]},name:"close",theme:"outlined"},a=n(9491),i=function(e,t){return o.createElement(a.Z,(0,r.Z)({},e,{ref:t,icon:c}))};var u=o.forwardRef(i)},1971:function(e,t,n){n.d(t,{Z:function(){return l},c:function(){return i}});var r=n(4942),o=n(9439),c=n(4519),a=n(1267),i=["xxl","xl","lg","md","sm","xs"],u=function(e){return{xs:"(max-width: ".concat(e.screenXSMax,"px)"),sm:"(min-width: ".concat(e.screenSM,"px)"),md:"(min-width: ".concat(e.screenMD,"px)"),lg:"(min-width: ".concat(e.screenLG,"px)"),xl:"(min-width: ".concat(e.screenXL,"px)"),xxl:"(min-width: ".concat(e.screenXXL,"px)")}},s=function(e){var t=e,n=[].concat(i).reverse();return n.forEach((function(e,r){var o=e.toUpperCase(),c="screen".concat(o,"Min"),a="screen".concat(o);if(!(t[c]<=t[a]))throw new Error("".concat(c,"<=").concat(a," fails : !(").concat(t[c],"<=").concat(t[a],")"));if(r<n.length-1){var i="screen".concat(o,"Max");if(!(t[a]<=t[i]))throw new Error("".concat(a,"<=").concat(i," fails : !(").concat(t[a],"<=").concat(t[i],")"));var u=n[r+1].toUpperCase(),s="screen".concat(u,"Min");if(!(t[i]<=t[s]))throw new Error("".concat(i,"<=").concat(s," fails : !(").concat(t[i],"<=").concat(t[s],")"))}})),e};function l(){var e=(0,a.Z)(),t=(0,o.Z)(e,2)[1],n=u(s(t));return c.useMemo((function(){var e=new Map,t=-1,o={};return{matchHandlers:{},dispatch:function(t){return o=t,e.forEach((function(e){return e(o)})),e.size>=1},subscribe:function(n){return e.size||this.register(),t+=1,e.set(t,n),n(o),t},unsubscribe:function(t){e.delete(t),e.size||this.unregister()},unregister:function(){var t=this;Object.keys(n).forEach((function(e){var r=n[e],o=t.matchHandlers[r];null===o||void 0===o||o.mql.removeListener(null===o||void 0===o?void 0:o.listener)})),e.clear()},register:function(){var e=this;Object.keys(n).forEach((function(t){var c=n[t],a=function(n){var c=n.matches;e.dispatch(Object.assign(Object.assign({},o),(0,r.Z)({},t,c)))},i=window.matchMedia(c);i.addListener(a),e.matchHandlers[c]={mql:i,listener:a},a(i)}))},responsiveMap:n}}),[t])}},9495:function(e,t,n){n.d(t,{Z:function(){return k}});var r=n(9439),o=n(3270),c=n.n(o),a=n(742),i=n(2145),u=n(4519),s=n(564),l=n(690),f=n(4942),d=n(111),v=function(e){var t=e.componentCls,n=e.colorPrimary;return(0,f.Z)({},t,{position:"absolute",background:"transparent",pointerEvents:"none",boxSizing:"border-box",color:"var(--wave-color, ".concat(n,")"),boxShadow:"0 0 0 0 currentcolor",opacity:.2,"&.wave-motion-appear":{transition:["box-shadow 0.4s ".concat(e.motionEaseOutCirc),"opacity 2s ".concat(e.motionEaseOutCirc)].join(","),"&-active":{boxShadow:"0 0 0 6px currentcolor",opacity:0},"&.wave-quick":{transition:["box-shadow 0.3s ".concat(e.motionEaseInOut),"opacity 0.35s ".concat(e.motionEaseInOut)].join(",")}}})},p=(0,d.Z)("Wave",(function(e){return[v(e)]})),m=n(4586),h=n(2058),b=n(6114),w=n(1277);function x(e){return e&&"#fff"!==e&&"#ffffff"!==e&&"rgb(255, 255, 255)"!==e&&"rgba(255, 255, 255, 1)"!==e&&function(e){var t=(e||"").match(/rgba?\((\d*), (\d*), (\d*)(, [\d.]*)?\)/);return!(t&&t[1]&&t[2]&&t[3])||!(t[1]===t[2]&&t[2]===t[3])}(e)&&!/rgba\((?:\d*, ){3}0\)/.test(e)&&"transparent"!==e}var Z=n(2967);function g(e){return Number.isNaN(e)?0:e}var E=function(e){var t=e.className,n=e.target,o=e.component,a=u.useRef(null),i=u.useState(null),s=(0,r.Z)(i,2),l=s[0],f=s[1],d=u.useState([]),v=(0,r.Z)(d,2),p=v[0],m=v[1],E=u.useState(0),y=(0,r.Z)(E,2),_=y[0],k=y[1],C=u.useState(0),L=(0,r.Z)(C,2),R=L[0],S=L[1],N=u.useState(0),O=(0,r.Z)(N,2),M=O[0],T=O[1],j=u.useState(0),A=(0,r.Z)(j,2),z=A[0],q=A[1],I=u.useState(!1),B=(0,r.Z)(I,2),P=B[0],W=B[1],D={left:_,top:R,width:M,height:z,borderRadius:p.map((function(e){return"".concat(e,"px")})).join(" ")};function F(){var e=getComputedStyle(n);f(function(e){var t=getComputedStyle(e),n=t.borderTopColor,r=t.borderColor,o=t.backgroundColor;return x(n)?n:x(r)?r:x(o)?o:null}(n));var t="static"===e.position,r=e.borderLeftWidth,o=e.borderTopWidth;k(t?n.offsetLeft:g(-parseFloat(r))),S(t?n.offsetTop:g(-parseFloat(o))),T(n.offsetWidth),q(n.offsetHeight);var c=e.borderTopLeftRadius,a=e.borderTopRightRadius,i=e.borderBottomLeftRadius,u=e.borderBottomRightRadius;m([c,a,u,i].map((function(e){return g(parseFloat(e))})))}if(l&&(D["--wave-color"]=l),u.useEffect((function(){if(n){var e,t=(0,h.Z)((function(){F(),W(!0)}));return"undefined"!==typeof ResizeObserver&&(e=new ResizeObserver(F)).observe(n),function(){h.Z.cancel(t),null===e||void 0===e||e.disconnect()}}}),[]),!P)return null;var H=("Checkbox"===o||"Radio"===o)&&(null===n||void 0===n?void 0:n.classList.contains(Z.A));return u.createElement(b.ZP,{visible:!0,motionAppear:!0,motionName:"wave-motion",motionDeadline:5e3,onAppearEnd:function(e,t){var n;if(t.deadline||"opacity"===t.propertyName){var r=null===(n=a.current)||void 0===n?void 0:n.parentElement;(0,w.v)(r).then((function(){null===r||void 0===r||r.remove()}))}return!1}},(function(e){var n=e.className;return u.createElement("div",{ref:a,className:c()(t,{"wave-quick":H},n),style:D})}))},y=function(e,t){var n;if("Checkbox"!==t.component||(null===(n=e.querySelector("input"))||void 0===n?void 0:n.checked)){var r=document.createElement("div");r.style.position="absolute",r.style.left="0px",r.style.top="0px",null===e||void 0===e||e.insertBefore(r,null===e||void 0===e?void 0:e.firstChild),(0,w.s)(u.createElement(E,Object.assign({},t,{target:e})),r)}},_=n(1267);var k=function(e){var t=e.children,n=e.disabled,o=e.component,f=(0,u.useContext)(s.E_).getPrefixCls,d=(0,u.useRef)(null),v=f("wave"),b=p(v),w=(0,r.Z)(b,2)[1],x=function(e,t,n){var o=u.useContext(s.E_).wave,c=(0,_.Z)(),a=(0,r.Z)(c,3),i=a[1],l=a[2],f=(0,m.Z)((function(r){var c=e.current;if(!(null===o||void 0===o?void 0:o.disabled)&&c){var a=c.querySelector(".".concat(Z.A))||c;((o||{}).showEffect||y)(a,{className:t,token:i,component:n,event:r,hashId:l})}})),d=u.useRef();return function(e){h.Z.cancel(d.current),d.current=(0,h.Z)((function(){f(e)}))}}(d,c()(v,w),o);if(u.useEffect((function(){var e=d.current;if(e&&1===e.nodeType&&!n){var t=function(t){!(0,i.Z)(t.target)||!e.getAttribute||e.getAttribute("disabled")||e.disabled||e.className.includes("disabled")||e.className.includes("-leave")||x(t)};return e.addEventListener("click",t,!0),function(){e.removeEventListener("click",t,!0)}}}),[n]),!u.isValidElement(t))return null!==t&&void 0!==t?t:null;var g=(0,a.Yr)(t)?(0,a.sQ)(t.ref,d):d;return(0,l.Tm)(t,{ref:g})}},2967:function(e,t,n){n.d(t,{A:function(){return r}});var r="ant-wave-target"},1277:function(e,t,n){var r;n.d(t,{s:function(){return h},v:function(){return Z}});var o,c=n(4165),a=n(5861),i=n(1002),u=n(1413),s=n(4453),l=(0,u.Z)({},r||(r=n.t(s,2))),f=l.version,d=l.render,v=l.unmountComponentAtNode;try{Number((f||"").split(".")[0])>=18&&(o=l.createRoot)}catch(E){}function p(e){var t=l.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;t&&"object"===(0,i.Z)(t)&&(t.usingClientEntryPoint=e)}var m="__rc_react_root__";function h(e,t){o?function(e,t){p(!0);var n=t[m]||o(t);p(!1),n.render(e),t[m]=n}(e,t):function(e,t){d(e,t)}(e,t)}function b(e){return w.apply(this,arguments)}function w(){return(w=(0,a.Z)((0,c.Z)().mark((function e(t){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",Promise.resolve().then((function(){var e;null===(e=t[m])||void 0===e||e.unmount(),delete t[m]})));case 1:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function x(e){v(e)}function Z(e){return g.apply(this,arguments)}function g(){return(g=(0,a.Z)((0,c.Z)().mark((function e(t){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(void 0===o){e.next=2;break}return e.abrupt("return",b(t));case 2:x(t);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}}}]);
//# sourceMappingURL=588.06dac2ee.chunk.js.map