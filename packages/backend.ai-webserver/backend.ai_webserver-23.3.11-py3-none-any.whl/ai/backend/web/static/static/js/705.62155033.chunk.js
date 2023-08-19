"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[705],{1662:function(e,t,n){n.d(t,{Z:function(){return l}});var o=n(7462),r=n(4519),c={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M563.8 512l262.5-312.9c4.4-5.2.7-13.1-6.1-13.1h-79.8c-4.7 0-9.2 2.1-12.3 5.7L511.6 449.8 295.1 191.7c-3-3.6-7.5-5.7-12.3-5.7H203c-6.8 0-10.5 7.9-6.1 13.1L459.4 512 196.9 824.9A7.95 7.95 0 00203 838h79.8c4.7 0 9.2-2.1 12.3-5.7l216.5-258.1 216.5 258.1c3 3.6 7.5 5.7 12.3 5.7h79.8c6.8 0 10.5-7.9 6.1-13.1L563.8 512z"}}]},name:"close",theme:"outlined"},a=n(9491),i=function(e,t){return r.createElement(a.Z,(0,o.Z)({},e,{ref:t,icon:c}))};var l=r.forwardRef(i)},3971:function(e,t,n){n.d(t,{Z:function(){return l}});var o=n(7462),r=n(4519),c={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M464 720a48 48 0 1096 0 48 48 0 10-96 0zm16-304v184c0 4.4 3.6 8 8 8h48c4.4 0 8-3.6 8-8V416c0-4.4-3.6-8-8-8h-48c-4.4 0-8 3.6-8 8zm475.7 440l-416-720c-6.2-10.7-16.9-16-27.7-16s-21.6 5.3-27.7 16l-416 720C56 877.4 71.4 904 96 904h832c24.6 0 40-26.6 27.7-48zm-783.5-27.9L512 239.9l339.8 588.2H172.2z"}}]},name:"warning",theme:"outlined"},a=n(9491),i=function(e,t){return r.createElement(a.Z,(0,o.Z)({},e,{ref:t,icon:c}))};var l=r.forwardRef(i)},9869:function(e,t,n){n.d(t,{Z:function(){return c}});var o=n(1662),r=n(4519);function c(e,t,n){var c=arguments.length>3&&void 0!==arguments[3]?arguments[3]:r.createElement(o.Z,null),a=function(e,t,n){return"boolean"===typeof e?e:void 0===t?!!n:!1!==t&&null!==t}(e,t,arguments.length>4&&void 0!==arguments[4]&&arguments[4]);if(!a)return[!1,null];var i="boolean"===typeof t||void 0===t||null===t?c:t;return[!0,n?n(i):i]}},145:function(e,t,n){var o=n(9439),r=n(4519),c=n(5706);t.Z=function(){var e=r.useState(!1),t=(0,o.Z)(e,2),n=t[0],a=t[1];return r.useEffect((function(){a((0,c.fk)())}),[]),n}},1971:function(e,t,n){n.d(t,{Z:function(){return u},c:function(){return i}});var o=n(4942),r=n(9439),c=n(4519),a=n(1267),i=["xxl","xl","lg","md","sm","xs"],l=function(e){return{xs:"(max-width: ".concat(e.screenXSMax,"px)"),sm:"(min-width: ".concat(e.screenSM,"px)"),md:"(min-width: ".concat(e.screenMD,"px)"),lg:"(min-width: ".concat(e.screenLG,"px)"),xl:"(min-width: ".concat(e.screenXL,"px)"),xxl:"(min-width: ".concat(e.screenXXL,"px)")}},s=function(e){var t=e,n=[].concat(i).reverse();return n.forEach((function(e,o){var r=e.toUpperCase(),c="screen".concat(r,"Min"),a="screen".concat(r);if(!(t[c]<=t[a]))throw new Error("".concat(c,"<=").concat(a," fails : !(").concat(t[c],"<=").concat(t[a],")"));if(o<n.length-1){var i="screen".concat(r,"Max");if(!(t[a]<=t[i]))throw new Error("".concat(a,"<=").concat(i," fails : !(").concat(t[a],"<=").concat(t[i],")"));var l=n[o+1].toUpperCase(),s="screen".concat(l,"Min");if(!(t[i]<=t[s]))throw new Error("".concat(i,"<=").concat(s," fails : !(").concat(t[i],"<=").concat(t[s],")"))}})),e};function u(){var e=(0,a.Z)(),t=(0,r.Z)(e,2)[1],n=l(s(t));return c.useMemo((function(){var e=new Map,t=-1,r={};return{matchHandlers:{},dispatch:function(t){return r=t,e.forEach((function(e){return e(r)})),e.size>=1},subscribe:function(n){return e.size||this.register(),t+=1,e.set(t,n),n(r),t},unsubscribe:function(t){e.delete(t),e.size||this.unregister()},unregister:function(){var t=this;Object.keys(n).forEach((function(e){var o=n[e],r=t.matchHandlers[o];null===r||void 0===r||r.mql.removeListener(null===r||void 0===r?void 0:r.listener)})),e.clear()},register:function(){var e=this;Object.keys(n).forEach((function(t){var c=n[t],a=function(n){var c=n.matches;e.dispatch(Object.assign(Object.assign({},r),(0,o.Z)({},t,c)))},i=window.matchMedia(c);i.addListener(a),e.matchHandlers[c]={mql:i,listener:a},a(i)}))},responsiveMap:n}}),[t])}},5706:function(e,t,n){n.d(t,{fk:function(){return a},jD:function(){return c}});var o,r=n(9001),c=function(){return(0,r.Z)()&&window.document.documentElement},a=function(){if(!c())return!1;if(void 0!==o)return o;var e=document.createElement("div");e.style.display="flex",e.style.flexDirection="column",e.style.rowGap="1px",e.appendChild(document.createElement("div")),e.appendChild(document.createElement("div"));var t=document.createElement("div");return t.style.position="absolute",t.style.zIndex="-9999",t.appendChild(e),document.body.appendChild(t),o=1===e.scrollHeight,document.body.removeChild(t),o}},9495:function(e,t,n){n.d(t,{Z:function(){return C}});var o=n(9439),r=n(3270),c=n.n(r),a=n(742),i=n(2145),l=n(4519),s=n(564),u=n(690),d=n(4942),f=n(111),p=function(e){var t=e.componentCls,n=e.colorPrimary;return(0,d.Z)({},t,{position:"absolute",background:"transparent",pointerEvents:"none",boxSizing:"border-box",color:"var(--wave-color, ".concat(n,")"),boxShadow:"0 0 0 0 currentcolor",opacity:.2,"&.wave-motion-appear":{transition:["box-shadow 0.4s ".concat(e.motionEaseOutCirc),"opacity 2s ".concat(e.motionEaseOutCirc)].join(","),"&-active":{boxShadow:"0 0 0 6px currentcolor",opacity:0}}})},m=(0,f.Z)("Wave",(function(e){return[p(e)]})),b=n(4278),v=n(1277),g=n(2058);function h(e){return e&&"#fff"!==e&&"#ffffff"!==e&&"rgb(255, 255, 255)"!==e&&"rgba(255, 255, 255, 1)"!==e&&function(e){var t=(e||"").match(/rgba?\((\d*), (\d*), (\d*)(, [\d.]*)?\)/);return!(t&&t[1]&&t[2]&&t[3])||!(t[1]===t[2]&&t[2]===t[3])}(e)&&!/rgba\((?:\d*, ){3}0\)/.test(e)&&"transparent"!==e}function y(e){return Number.isNaN(e)?0:e}var x=function(e){var t=e.className,n=e.target,r=l.useRef(null),a=l.useState(null),i=(0,o.Z)(a,2),s=i[0],u=i[1],d=l.useState([]),f=(0,o.Z)(d,2),p=f[0],m=f[1],x=l.useState(0),Z=(0,o.Z)(x,2),C=Z[0],S=Z[1],w=l.useState(0),O=(0,o.Z)(w,2),E=O[0],j=O[1],k=l.useState(0),N=(0,o.Z)(k,2),P=N[0],L=N[1],I=l.useState(0),T=(0,o.Z)(I,2),M=T[0],z=T[1],B=l.useState(!1),R=(0,o.Z)(B,2),_=R[0],W=R[1],H={left:C,top:E,width:P,height:M,borderRadius:p.map((function(e){return"".concat(e,"px")})).join(" ")};function A(){var e=getComputedStyle(n);u(function(e){var t=getComputedStyle(e),n=t.borderTopColor,o=t.borderColor,r=t.backgroundColor;return h(n)?n:h(o)?o:h(r)?r:null}(n));var t="static"===e.position,o=e.borderLeftWidth,r=e.borderTopWidth;S(t?n.offsetLeft:y(-parseFloat(o))),j(t?n.offsetTop:y(-parseFloat(r))),L(n.offsetWidth),z(n.offsetHeight);var c=e.borderTopLeftRadius,a=e.borderTopRightRadius,i=e.borderBottomLeftRadius,l=e.borderBottomRightRadius;m([c,a,l,i].map((function(e){return y(parseFloat(e))})))}return s&&(H["--wave-color"]=s),l.useEffect((function(){if(n){var e,t=(0,g.Z)((function(){A(),W(!0)}));return"undefined"!==typeof ResizeObserver&&(e=new ResizeObserver(A)).observe(n),function(){g.Z.cancel(t),null===e||void 0===e||e.disconnect()}}}),[]),_?l.createElement(b.ZP,{visible:!0,motionAppear:!0,motionName:"wave-motion",motionDeadline:5e3,onAppearEnd:function(e,t){var n;if(t.deadline||"opacity"===t.propertyName){var o=null===(n=r.current)||void 0===n?void 0:n.parentElement;(0,v.v)(o).then((function(){null===o||void 0===o||o.remove()}))}return!1}},(function(e){var n=e.className;return l.createElement("div",{ref:r,className:c()(t,n),style:H})})):null};function Z(e,t){return function(){!function(e,t){var n=document.createElement("div");n.style.position="absolute",n.style.left="0px",n.style.top="0px",null===e||void 0===e||e.insertBefore(n,null===e||void 0===e?void 0:e.firstChild),(0,v.s)(l.createElement(x,{target:e,className:t}),n)}(e.current,t)}}var C=function(e){var t=e.children,n=e.disabled,r=(0,l.useContext)(s.E_).getPrefixCls,d=(0,l.useRef)(null),f=r("wave"),p=m(f),b=(0,o.Z)(p,2)[1],v=Z(d,c()(f,b));if(l.useEffect((function(){var e=d.current;if(e&&1===e.nodeType&&!n){var t=function(t){"INPUT"===t.target.tagName||!(0,i.Z)(t.target)||!e.getAttribute||e.getAttribute("disabled")||e.disabled||e.className.includes("disabled")||e.className.includes("-leave")||v()};return e.addEventListener("click",t,!0),function(){e.removeEventListener("click",t,!0)}}}),[n]),!l.isValidElement(t))return null!==t&&void 0!==t?t:null;var g=(0,a.Yr)(t)?(0,a.sQ)(t.ref,d):d;return(0,u.Tm)(t,{ref:g})}},2704:function(e,t,n){var o=n(6038);t.Z=o.Z},3678:function(e,t,n){n.d(t,{Z:function(){return k}});var o=n(4942),r=n(9439),c=n(3270),a=n.n(c),i=n(5882),l=n(4519),s=n(690),u=n(1971),d=n(564),f=n(6569),p=l.createContext({}),m=function(e){return e.children};function b(e){return void 0!==e&&null!==e}var v=function(e){var t,n=e.itemPrefixCls,r=e.component,c=e.span,i=e.className,s=e.style,u=e.labelStyle,d=e.contentStyle,f=e.bordered,p=e.label,m=e.content,v=e.colon,g=r;return f?l.createElement(g,{className:a()((t={},(0,o.Z)(t,"".concat(n,"-item-label"),b(p)),(0,o.Z)(t,"".concat(n,"-item-content"),b(m)),t),i),style:s,colSpan:c},b(p)&&l.createElement("span",{style:u},p),b(m)&&l.createElement("span",{style:d},m)):l.createElement(g,{className:a()("".concat(n,"-item"),i),style:s,colSpan:c},l.createElement("div",{className:"".concat(n,"-item-container")},(p||0===p)&&l.createElement("span",{className:a()("".concat(n,"-item-label"),(0,o.Z)({},"".concat(n,"-item-no-colon"),!v)),style:u},p),(m||0===m)&&l.createElement("span",{className:a()("".concat(n,"-item-content")),style:d},m)))};function g(e,t,n){var o=t.colon,r=t.prefixCls,c=t.bordered,a=n.component,i=n.type,s=n.showLabel,u=n.showContent,d=n.labelStyle,f=n.contentStyle;return e.map((function(e,t){var n=e.props,p=n.label,m=n.children,b=n.prefixCls,g=void 0===b?r:b,h=n.className,y=n.style,x=n.labelStyle,Z=n.contentStyle,C=n.span,S=void 0===C?1:C,w=e.key;return"string"===typeof a?l.createElement(v,{key:"".concat(i,"-").concat(w||t),className:h,style:y,labelStyle:Object.assign(Object.assign({},d),x),contentStyle:Object.assign(Object.assign({},f),Z),span:S,colon:o,component:a,itemPrefixCls:g,bordered:c,label:s?p:null,content:u?m:null}):[l.createElement(v,{key:"label-".concat(w||t),className:h,style:Object.assign(Object.assign(Object.assign({},d),y),x),span:1,colon:o,component:a[0],itemPrefixCls:g,bordered:c,label:p}),l.createElement(v,{key:"content-".concat(w||t),className:h,style:Object.assign(Object.assign(Object.assign({},f),y),Z),span:2*S-1,component:a[1],itemPrefixCls:g,bordered:c,content:m})]}))}var h=function(e){var t=l.useContext(p),n=e.prefixCls,o=e.vertical,r=e.row,c=e.index,a=e.bordered;return o?l.createElement(l.Fragment,null,l.createElement("tr",{key:"label-".concat(c),className:"".concat(n,"-row")},g(r,e,Object.assign({component:"th",type:"label",showLabel:!0},t))),l.createElement("tr",{key:"content-".concat(c),className:"".concat(n,"-row")},g(r,e,Object.assign({component:"td",type:"content",showContent:!0},t)))):l.createElement("tr",{key:c,className:"".concat(n,"-row")},g(r,e,Object.assign({component:a?["th","td"]:"td",type:"item",showLabel:!0,showContent:!0},t)))},y=n(1480),x=n(111),Z=n(1157),C=function(e){var t,n,r=e.componentCls,c=e.extraColor,a=e.itemPaddingBottom,i=e.colonMarginRight,l=e.colonMarginLeft,s=e.titleMarginBottom;return(0,o.Z)({},r,Object.assign(Object.assign(Object.assign({},(0,y.Wf)(e)),function(e){var t,n=e.componentCls,r=e.labelBg;return(0,o.Z)({},"&".concat(n,"-bordered"),(t={},(0,o.Z)(t,"".concat(n,"-view"),{border:"".concat(e.lineWidth,"px ").concat(e.lineType," ").concat(e.colorSplit),"> table":{tableLayout:"auto",borderCollapse:"collapse"}}),(0,o.Z)(t,"".concat(n,"-item-label, ").concat(n,"-item-content"),{padding:"".concat(e.padding,"px ").concat(e.paddingLG,"px"),borderInlineEnd:"".concat(e.lineWidth,"px ").concat(e.lineType," ").concat(e.colorSplit),"&:last-child":{borderInlineEnd:"none"}}),(0,o.Z)(t,"".concat(n,"-item-label"),{color:e.colorTextSecondary,backgroundColor:r,"&::after":{display:"none"}}),(0,o.Z)(t,"".concat(n,"-row"),{borderBottom:"".concat(e.lineWidth,"px ").concat(e.lineType," ").concat(e.colorSplit),"&:last-child":{borderBottom:"none"}}),(0,o.Z)(t,"&".concat(n,"-middle"),(0,o.Z)({},"".concat(n,"-item-label, ").concat(n,"-item-content"),{padding:"".concat(e.paddingSM,"px ").concat(e.paddingLG,"px")})),(0,o.Z)(t,"&".concat(n,"-small"),(0,o.Z)({},"".concat(n,"-item-label, ").concat(n,"-item-content"),{padding:"".concat(e.paddingXS,"px ").concat(e.padding,"px")})),t))}(e)),(n={},(0,o.Z)(n,"&-rtl",{direction:"rtl"}),(0,o.Z)(n,"".concat(r,"-header"),{display:"flex",alignItems:"center",marginBottom:s}),(0,o.Z)(n,"".concat(r,"-title"),Object.assign(Object.assign({},y.vS),{flex:"auto",color:e.colorText,fontWeight:e.fontWeightStrong,fontSize:e.fontSizeLG,lineHeight:e.lineHeightLG})),(0,o.Z)(n,"".concat(r,"-extra"),{marginInlineStart:"auto",color:c,fontSize:e.fontSize}),(0,o.Z)(n,"".concat(r,"-view"),{width:"100%",borderRadius:e.borderRadiusLG,table:{width:"100%",tableLayout:"fixed"}}),(0,o.Z)(n,"".concat(r,"-row"),{"> th, > td":{paddingBottom:a},"&:last-child":{borderBottom:"none"}}),(0,o.Z)(n,"".concat(r,"-item-label"),(0,o.Z)({color:e.colorTextTertiary,fontWeight:"normal",fontSize:e.fontSize,lineHeight:e.lineHeight,textAlign:"start","&::after":{content:'":"',position:"relative",top:-.5,marginInline:"".concat(l,"px ").concat(i,"px")}},"&".concat(r,"-item-no-colon::after"),{content:'""'})),(0,o.Z)(n,"".concat(r,"-item-no-label"),{"&::after":{margin:0,content:'""'}}),(0,o.Z)(n,"".concat(r,"-item-content"),{display:"table-cell",flex:1,color:e.colorText,fontSize:e.fontSize,lineHeight:e.lineHeight,wordBreak:"break-word",overflowWrap:"break-word"}),(0,o.Z)(n,"".concat(r,"-item"),{paddingBottom:0,verticalAlign:"top","&-container":(t={display:"flex"},(0,o.Z)(t,"".concat(r,"-item-label"),{display:"inline-flex",alignItems:"baseline"}),(0,o.Z)(t,"".concat(r,"-item-content"),{display:"inline-flex",alignItems:"baseline"}),t)}),(0,o.Z)(n,"&-middle",(0,o.Z)({},"".concat(r,"-row"),{"> th, > td":{paddingBottom:e.paddingSM}})),(0,o.Z)(n,"&-small",(0,o.Z)({},"".concat(r,"-row"),{"> th, > td":{paddingBottom:e.paddingXS}})),n)))},S=(0,x.Z)("Descriptions",(function(e){var t=(0,Z.TS)(e,{});return[C(t)]}),(function(e){return{labelBg:e.colorFillAlter,titleMarginBottom:e.fontSizeSM*e.lineHeightSM,itemPaddingBottom:e.padding,colonMarginRight:e.marginXS,colonMarginLeft:e.marginXXS/2,extraColor:e.colorText}})),w=function(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)t.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(n[o[r]]=e[o[r]])}return n},O={xxl:3,xl:3,lg:3,md:3,sm:2,xs:1};function E(e,t,n){var o=e;return(void 0===n||n>t)&&(o=(0,s.Tm)(e,{span:t})),o}var j=function(e){var t,n=e.prefixCls,c=e.title,s=e.extra,m=e.column,b=void 0===m?O:m,v=e.colon,g=void 0===v||v,y=e.bordered,x=e.layout,Z=e.children,C=e.className,j=e.rootClassName,k=e.style,N=e.size,P=e.labelStyle,L=e.contentStyle,I=w(e,["prefixCls","title","extra","column","colon","bordered","layout","children","className","rootClassName","style","size","labelStyle","contentStyle"]),T=l.useContext(d.E_),M=T.getPrefixCls,z=T.direction,B=T.descriptions,R=M("descriptions",n),_=l.useState({}),W=(0,r.Z)(_,2),H=W[0],A=W[1],F=function(e,t){if("number"===typeof e)return e;if("object"===typeof e)for(var n=0;n<u.c.length;n++){var o=u.c[n];if(t[o]&&void 0!==e[o])return e[o]||O[o]}return 3}(b,H),X=(0,f.Z)(N),G=S(R),D=(0,r.Z)(G,2),U=D[0],V=D[1],q=(0,u.Z)();l.useEffect((function(){var e=q.subscribe((function(e){"object"===typeof b&&A(e)}));return function(){q.unsubscribe(e)}}),[]);var Q=function(e,t){var n=(0,i.Z)(e).filter((function(e){return e})),o=[],r=[],c=t;return n.forEach((function(e,a){var i,l=null===(i=e.props)||void 0===i?void 0:i.span,s=l||1;if(a===n.length-1)return r.push(E(e,c,l)),void o.push(r);s<c?(c-=s,r.push(e)):(r.push(E(e,c,s)),o.push(r),c=t,r=[])})),o}(Z,F),Y=l.useMemo((function(){return{labelStyle:P,contentStyle:L}}),[P,L]);return U(l.createElement(p.Provider,{value:Y},l.createElement("div",Object.assign({className:a()(R,null===B||void 0===B?void 0:B.className,(t={},(0,o.Z)(t,"".concat(R,"-").concat(X),X&&"default"!==X),(0,o.Z)(t,"".concat(R,"-bordered"),!!y),(0,o.Z)(t,"".concat(R,"-rtl"),"rtl"===z),t),C,j,V),style:Object.assign(Object.assign({},null===B||void 0===B?void 0:B.style),k)},I),(c||s)&&l.createElement("div",{className:"".concat(R,"-header")},c&&l.createElement("div",{className:"".concat(R,"-title")},c),s&&l.createElement("div",{className:"".concat(R,"-extra")},s)),l.createElement("div",{className:"".concat(R,"-view")},l.createElement("table",null,l.createElement("tbody",null,Q.map((function(e,t){return l.createElement(h,{key:t,index:t,colon:g,prefixCls:R,vertical:"vertical"===x,bordered:y,row:e})}))))))))};j.Item=m;var k=j},8945:function(e,t,n){var o=(0,n(4519).createContext)({});t.Z=o},6038:function(e,t,n){var o=n(4942),r=n(9439),c=n(3270),a=n.n(c),i=n(4519),l=n(564),s=n(8945),u=n(2861),d=function(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)t.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(n[o[r]]=e[o[r]])}return n};var f=["xs","sm","md","lg","xl","xxl"],p=i.forwardRef((function(e,t){var n,c=i.useContext(l.E_),p=c.getPrefixCls,m=c.direction,b=i.useContext(s.Z),v=b.gutter,g=b.wrap,h=b.supportFlexGap,y=e.prefixCls,x=e.span,Z=e.order,C=e.offset,S=e.push,w=e.pull,O=e.className,E=e.children,j=e.flex,k=e.style,N=d(e,["prefixCls","span","order","offset","push","pull","className","children","flex","style"]),P=p("col",y),L=(0,u.c)(P),I=(0,r.Z)(L,2),T=I[0],M=I[1],z={};f.forEach((function(t){var n,r={},c=e[t];"number"===typeof c?r.span=c:"object"===typeof c&&(r=c||{}),delete N[t],z=Object.assign(Object.assign({},z),(n={},(0,o.Z)(n,"".concat(P,"-").concat(t,"-").concat(r.span),void 0!==r.span),(0,o.Z)(n,"".concat(P,"-").concat(t,"-order-").concat(r.order),r.order||0===r.order),(0,o.Z)(n,"".concat(P,"-").concat(t,"-offset-").concat(r.offset),r.offset||0===r.offset),(0,o.Z)(n,"".concat(P,"-").concat(t,"-push-").concat(r.push),r.push||0===r.push),(0,o.Z)(n,"".concat(P,"-").concat(t,"-pull-").concat(r.pull),r.pull||0===r.pull),(0,o.Z)(n,"".concat(P,"-").concat(t,"-flex-").concat(r.flex),r.flex||"auto"===r.flex),(0,o.Z)(n,"".concat(P,"-rtl"),"rtl"===m),n))}));var B=a()(P,(n={},(0,o.Z)(n,"".concat(P,"-").concat(x),void 0!==x),(0,o.Z)(n,"".concat(P,"-order-").concat(Z),Z),(0,o.Z)(n,"".concat(P,"-offset-").concat(C),C),(0,o.Z)(n,"".concat(P,"-push-").concat(S),S),(0,o.Z)(n,"".concat(P,"-pull-").concat(w),w),n),O,z,M),R={};if(v&&v[0]>0){var _=v[0]/2;R.paddingLeft=_,R.paddingRight=_}if(v&&v[1]>0&&!h){var W=v[1]/2;R.paddingTop=W,R.paddingBottom=W}return j&&(R.flex=function(e){return"number"===typeof e?"".concat(e," ").concat(e," auto"):/^\d+(\.\d+)?(px|em|rem|%)$/.test(e)?"0 0 ".concat(e):e}(j),!1!==g||R.minWidth||(R.minWidth=0)),T(i.createElement("div",Object.assign({},N,{style:Object.assign(Object.assign({},R),k),className:B,ref:t}),E))}));t.Z=p},1718:function(e,t,n){var o=n(4942),r=n(9439),c=n(3270),a=n.n(c),i=n(4519),l=n(564),s=n(145),u=n(1971),d=n(8945),f=n(2861),p=function(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)t.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(n[o[r]]=e[o[r]])}return n};function m(e,t){var n=i.useState("string"===typeof e?e:""),o=(0,r.Z)(n,2),c=o[0],a=o[1];return i.useEffect((function(){!function(){if("string"===typeof e&&a(e),"object"===typeof e)for(var n=0;n<u.c.length;n++){var o=u.c[n];if(t[o]){var r=e[o];if(void 0!==r)return void a(r)}}}()}),[JSON.stringify(e),t]),c}var b=i.forwardRef((function(e,t){var n,c=e.prefixCls,b=e.justify,v=e.align,g=e.className,h=e.style,y=e.children,x=e.gutter,Z=void 0===x?0:x,C=e.wrap,S=p(e,["prefixCls","justify","align","className","style","children","gutter","wrap"]),w=i.useContext(l.E_),O=w.getPrefixCls,E=w.direction,j=i.useState({xs:!0,sm:!0,md:!0,lg:!0,xl:!0,xxl:!0}),k=(0,r.Z)(j,2),N=k[0],P=k[1],L=i.useState({xs:!1,sm:!1,md:!1,lg:!1,xl:!1,xxl:!1}),I=(0,r.Z)(L,2),T=I[0],M=I[1],z=m(v,T),B=m(b,T),R=(0,s.Z)(),_=i.useRef(Z),W=(0,u.Z)();i.useEffect((function(){var e=W.subscribe((function(e){M(e);var t=_.current||0;(!Array.isArray(t)&&"object"===typeof t||Array.isArray(t)&&("object"===typeof t[0]||"object"===typeof t[1]))&&P(e)}));return function(){return W.unsubscribe(e)}}),[]);var H=O("row",c),A=(0,f.V)(H),F=(0,r.Z)(A,2),X=F[0],G=F[1],D=function(){var e=[void 0,void 0];return(Array.isArray(Z)?Z:[Z,void 0]).forEach((function(t,n){if("object"===typeof t)for(var o=0;o<u.c.length;o++){var r=u.c[o];if(N[r]&&void 0!==t[r]){e[n]=t[r];break}}else e[n]=t})),e}(),U=a()(H,(n={},(0,o.Z)(n,"".concat(H,"-no-wrap"),!1===C),(0,o.Z)(n,"".concat(H,"-").concat(B),B),(0,o.Z)(n,"".concat(H,"-").concat(z),z),(0,o.Z)(n,"".concat(H,"-rtl"),"rtl"===E),n),g,G),V={},q=null!=D[0]&&D[0]>0?D[0]/-2:void 0,Q=null!=D[1]&&D[1]>0?D[1]/-2:void 0;if(q&&(V.marginLeft=q,V.marginRight=q),R){var Y=(0,r.Z)(D,2);V.rowGap=Y[1]}else Q&&(V.marginTop=Q,V.marginBottom=Q);var J=(0,r.Z)(D,2),$=J[0],K=J[1],ee=i.useMemo((function(){return{gutter:[$,K],wrap:C,supportFlexGap:R}}),[$,K,C,R]);return X(i.createElement(d.Z.Provider,{value:ee},i.createElement("div",Object.assign({},S,{className:U,style:Object.assign(Object.assign({},V),h),ref:t}),y)))}));t.Z=b},2861:function(e,t,n){n.d(t,{V:function(){return s},c:function(){return u}});var o=n(4942),r=n(111),c=n(1157),a=function(e){var t=e.componentCls;return(0,o.Z)({},t,{display:"flex",flexFlow:"row wrap",minWidth:0,"&::before, &::after":{display:"flex"},"&-no-wrap":{flexWrap:"nowrap"},"&-start":{justifyContent:"flex-start"},"&-center":{justifyContent:"center"},"&-end":{justifyContent:"flex-end"},"&-space-between":{justifyContent:"space-between"},"&-space-around":{justifyContent:"space-around"},"&-space-evenly":{justifyContent:"space-evenly"},"&-top":{alignItems:"flex-start"},"&-middle":{alignItems:"center"},"&-bottom":{alignItems:"flex-end"}})},i=function(e){var t=e.componentCls;return(0,o.Z)({},t,{position:"relative",maxWidth:"100%",minHeight:1})},l=function(e,t){return function(e,t){for(var n=e.componentCls,o=e.gridColumns,r={},c=o;c>=0;c--)0===c?(r["".concat(n).concat(t,"-").concat(c)]={display:"none"},r["".concat(n,"-push-").concat(c)]={insetInlineStart:"auto"},r["".concat(n,"-pull-").concat(c)]={insetInlineEnd:"auto"},r["".concat(n).concat(t,"-push-").concat(c)]={insetInlineStart:"auto"},r["".concat(n).concat(t,"-pull-").concat(c)]={insetInlineEnd:"auto"},r["".concat(n).concat(t,"-offset-").concat(c)]={marginInlineStart:0},r["".concat(n).concat(t,"-order-").concat(c)]={order:0}):(r["".concat(n).concat(t,"-").concat(c)]={display:"block",flex:"0 0 ".concat(c/o*100,"%"),maxWidth:"".concat(c/o*100,"%")},r["".concat(n).concat(t,"-push-").concat(c)]={insetInlineStart:"".concat(c/o*100,"%")},r["".concat(n).concat(t,"-pull-").concat(c)]={insetInlineEnd:"".concat(c/o*100,"%")},r["".concat(n).concat(t,"-offset-").concat(c)]={marginInlineStart:"".concat(c/o*100,"%")},r["".concat(n).concat(t,"-order-").concat(c)]={order:c});return r}(e,t)},s=(0,r.Z)("Grid",(function(e){return[a(e)]})),u=(0,r.Z)("Grid",(function(e){var t=(0,c.TS)(e,{gridColumns:24}),n={"-sm":t.screenSMMin,"-md":t.screenMDMin,"-lg":t.screenLGMin,"-xl":t.screenXLMin,"-xxl":t.screenXXLMin};return[i(t),l(t,""),l(t,"-xs"),Object.keys(n).map((function(e){return function(e,t,n){return(0,o.Z)({},"@media (min-width: ".concat(t,"px)"),Object.assign({},l(e,n)))}(t,n[e],e)})).reduce((function(e,t){return Object.assign(Object.assign({},e),t)}),{})]}))},5492:function(e,t,n){var o=n(1718);t.Z=o.Z},5870:function(e,t,n){n.d(t,{Z:function(){return E}});var o=n(4942),r=n(9439),c=n(1662),a=n(3270),i=n.n(a),l=n(4519),s=n(1235),u=n(9869),d=n(9495),f=n(564);var p=n(1480),m=n(150),b=n(111),v=n(1157),g=function(e,t,n){var r,c="string"!==typeof(r=n)?r:r.charAt(0).toUpperCase()+r.slice(1);return(0,o.Z)({},"".concat(e.componentCls,"-").concat(t),(0,o.Z)({color:e["color".concat(n)],background:e["color".concat(c,"Bg")],borderColor:e["color".concat(c,"Border")]},"&".concat(e.componentCls,"-borderless"),{borderColor:"transparent"}))},h=function(e){return(0,m.Z)(e,(function(t,n){var r=n.textColor,c=n.lightBorderColor,a=n.lightColor,i=n.darkColor;return(0,o.Z)({},"".concat(e.componentCls,"-").concat(t),(0,o.Z)({color:r,background:a,borderColor:c,"&-inverse":{color:e.colorTextLightSolid,background:i,borderColor:i}},"&".concat(e.componentCls,"-borderless"),{borderColor:"transparent"}))}))},y=function(e){var t,n,r,c=e.paddingXXS,a=e.lineWidth,i=e.tagPaddingHorizontal,l=e.componentCls,s=i-a,u=c-a;return r={},(0,o.Z)(r,l,Object.assign(Object.assign({},(0,p.Wf)(e)),(n={display:"inline-block",height:"auto",marginInlineEnd:e.marginXS,paddingInline:s,fontSize:e.tagFontSize,lineHeight:e.tagLineHeight,whiteSpace:"nowrap",background:e.defaultBg,border:"".concat(e.lineWidth,"px ").concat(e.lineType," ").concat(e.colorBorder),borderRadius:e.borderRadiusSM,opacity:1,transition:"all ".concat(e.motionDurationMid),textAlign:"start",position:"relative"},(0,o.Z)(n,"&".concat(l,"-rtl"),{direction:"rtl"}),(0,o.Z)(n,"&, a, a:hover",{color:e.defaultColor}),(0,o.Z)(n,"".concat(l,"-close-icon"),{marginInlineStart:u,color:e.colorTextDescription,fontSize:e.tagIconSize,cursor:"pointer",transition:"all ".concat(e.motionDurationMid),"&:hover":{color:e.colorTextHeading}}),(0,o.Z)(n,"&".concat(l,"-has-color"),(0,o.Z)({borderColor:"transparent"},"&, a, a:hover, ".concat(e.iconCls,"-close, ").concat(e.iconCls,"-close:hover"),{color:e.colorTextLightSolid})),(0,o.Z)(n,"&-checkable",(t={backgroundColor:"transparent",borderColor:"transparent",cursor:"pointer"},(0,o.Z)(t,"&:not(".concat(l,"-checkable-checked):hover"),{color:e.colorPrimary,backgroundColor:e.colorFillSecondary}),(0,o.Z)(t,"&:active, &-checked",{color:e.colorTextLightSolid}),(0,o.Z)(t,"&-checked",{backgroundColor:e.colorPrimary,"&:hover":{backgroundColor:e.colorPrimaryHover}}),(0,o.Z)(t,"&:active",{backgroundColor:e.colorPrimaryActive}),t)),(0,o.Z)(n,"&-hidden",{display:"none"}),(0,o.Z)(n,"> ".concat(e.iconCls," + span, > span + ").concat(e.iconCls),{marginInlineStart:s}),n))),(0,o.Z)(r,"".concat(l,"-borderless"),{borderColor:"transparent",background:e.tagBorderlessBg}),r},x=(0,b.Z)("Tag",(function(e){var t=e.lineWidth,n=e.fontSizeIcon,o=e.fontSizeSM,r="".concat(e.lineHeightSM*o,"px"),c=(0,v.TS)(e,{tagFontSize:o,tagLineHeight:r,tagIconSize:n-2*t,tagPaddingHorizontal:8,tagBorderlessBg:e.colorFillTertiary});return[y(c),h(c),g(c,"success","Success"),g(c,"processing","Info"),g(c,"error","Error"),g(c,"warning","Warning")]}),(function(e){return{defaultBg:e.colorFillQuaternary,defaultColor:e.colorText}})),Z=function(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)t.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(n[o[r]]=e[o[r]])}return n},C=function(e){var t=e.prefixCls,n=e.className,c=e.checked,a=e.onChange,s=e.onClick,u=Z(e,["prefixCls","className","checked","onChange","onClick"]),d=(0,l.useContext(f.E_).getPrefixCls)("tag",t),p=x(d),m=(0,r.Z)(p,2),b=m[0],v=m[1],g=i()(d,"".concat(d,"-checkable"),(0,o.Z)({},"".concat(d,"-checkable-checked"),c),n,v);return b(l.createElement("span",Object.assign({},u,{className:g,onClick:function(e){null===a||void 0===a||a(!c),null===s||void 0===s||s(e)}})))},S=function(e,t){var n={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&t.indexOf(o)<0&&(n[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)t.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(n[o[r]]=e[o[r]])}return n},w=function(e,t){var n,a=e.prefixCls,p=e.className,m=e.rootClassName,b=e.style,v=e.children,g=e.icon,h=e.color,y=e.onClose,Z=e.closeIcon,C=e.closable,w=e.bordered,O=void 0===w||w,E=S(e,["prefixCls","className","rootClassName","style","children","icon","color","onClose","closeIcon","closable","bordered"]),j=l.useContext(f.E_),k=j.getPrefixCls,N=j.direction,P=j.tag,L=l.useState(!0),I=(0,r.Z)(L,2),T=I[0],M=I[1];l.useEffect((function(){"visible"in E&&M(E.visible)}),[E.visible]);var z=(0,s.o2)(h)||(0,s.yT)(h),B=Object.assign(Object.assign({backgroundColor:h&&!z?h:void 0},null===P||void 0===P?void 0:P.style),b),R=k("tag",a),_=x(R),W=(0,r.Z)(_,2),H=W[0],A=W[1],F=i()(R,null===P||void 0===P?void 0:P.className,(n={},(0,o.Z)(n,"".concat(R,"-").concat(h),z),(0,o.Z)(n,"".concat(R,"-has-color"),h&&!z),(0,o.Z)(n,"".concat(R,"-hidden"),!T),(0,o.Z)(n,"".concat(R,"-rtl"),"rtl"===N),(0,o.Z)(n,"".concat(R,"-borderless"),!O),n),p,m,A),X=function(e){e.stopPropagation(),null===y||void 0===y||y(e),e.defaultPrevented||M(!1)},G=(0,u.Z)(C,Z,(function(e){return null===e?l.createElement(c.Z,{className:"".concat(R,"-close-icon"),onClick:X}):l.createElement("span",{className:"".concat(R,"-close-icon"),onClick:X},e)}),null,!1),D=(0,r.Z)(G,2)[1],U="function"===typeof E.onClick||v&&"a"===v.type,V=g||null,q=V?l.createElement(l.Fragment,null,V,v&&l.createElement("span",null,v)):v,Q=l.createElement("span",Object.assign({},E,{ref:t,className:F,style:B}),q,D);return H(U?l.createElement(d.Z,null,Q):Q)},O=l.forwardRef(w);O.CheckableTag=C;var E=O},1277:function(e,t,n){var o;n.d(t,{s:function(){return v},v:function(){return x}});var r,c=n(4165),a=n(5861),i=n(1002),l=n(1413),s=n(4453),u=(0,l.Z)({},o||(o=n.t(s,2))),d=u.version,f=u.render,p=u.unmountComponentAtNode;try{Number((d||"").split(".")[0])>=18&&(r=u.createRoot)}catch(C){}function m(e){var t=u.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED;t&&"object"===(0,i.Z)(t)&&(t.usingClientEntryPoint=e)}var b="__rc_react_root__";function v(e,t){r?function(e,t){m(!0);var n=t[b]||r(t);m(!1),n.render(e),t[b]=n}(e,t):function(e,t){f(e,t)}(e,t)}function g(e){return h.apply(this,arguments)}function h(){return(h=(0,a.Z)((0,c.Z)().mark((function e(t){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:return e.abrupt("return",Promise.resolve().then((function(){var e;null===(e=t[b])||void 0===e||e.unmount(),delete t[b]})));case 1:case"end":return e.stop()}}),e)})))).apply(this,arguments)}function y(e){p(e)}function x(e){return Z.apply(this,arguments)}function Z(){return(Z=(0,a.Z)((0,c.Z)().mark((function e(t){return(0,c.Z)().wrap((function(e){for(;;)switch(e.prev=e.next){case 0:if(void 0===r){e.next=2;break}return e.abrupt("return",g(t));case 2:y(t);case 3:case"end":return e.stop()}}),e)})))).apply(this,arguments)}}}]);
//# sourceMappingURL=705.62155033.chunk.js.map