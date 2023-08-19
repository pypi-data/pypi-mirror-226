"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[978],{6814:function(e,n,o){o.d(n,{Z:function(){return i}});var t=o(7462),r=o(4519),c={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M880 836H144c-17.7 0-32 14.3-32 32v36c0 4.4 3.6 8 8 8h784c4.4 0 8-3.6 8-8v-36c0-17.7-14.3-32-32-32zm-622.3-84c2 0 4-.2 6-.5L431.9 722c2-.4 3.9-1.3 5.3-2.8l423.9-423.9a9.96 9.96 0 000-14.1L694.9 114.9c-1.9-1.9-4.4-2.9-7.1-2.9s-5.2 1-7.1 2.9L256.8 538.8c-1.5 1.5-2.4 3.3-2.8 5.3l-29.5 168.2a33.5 33.5 0 009.4 29.8c6.6 6.4 14.9 9.9 23.8 9.9z"}}]},name:"edit",theme:"filled"},a=o(9491),l=function(e,n){return r.createElement(a.Z,(0,t.Z)({},e,{ref:n,icon:c}))};var i=r.forwardRef(l)},374:function(e,n,o){o.d(n,{Z:function(){return c}});Object.create;function t(e,n){var o="function"===typeof Symbol&&e[Symbol.iterator];if(!o)return e;var t,r,c=o.call(e),a=[];try{for(;(void 0===n||n-- >0)&&!(t=c.next()).done;)a.push(t.value)}catch(l){r={error:l}}finally{try{t&&!t.done&&(o=c.return)&&o.call(c)}finally{if(r)throw r.error}}return a}Object.create;var r=o(4519);var c=function(e,n){void 0===e&&(e=!1);var o=t((0,r.useState)(e),2),c=o[0],a=o[1];return[c,(0,r.useMemo)((function(){var o=void 0===n?!e:n;return{toggle:function(){return a((function(n){return n===e?o:e}))},set:function(e){return a(e)},setLeft:function(){return a(e)},setRight:function(){return a(o)}}}),[])]}},1366:function(e,n,o){o.d(n,{Z:function(){return N}});var t=o(9439),r=o(8724),c=o(3270),a=o.n(c),l=o(3714),i=o(269),s=o(4325),u=o(4519),d=o(690),p=o(564),f=o(6524),g=o(9014),m=o(7127),v=o(2513),b=o(2187),C=o(6951),y=o(8557),h=o(1289),Z=o(4942),x=o(111),O=(0,x.Z)("Popconfirm",(function(e){return function(e){var n,o,t=e.componentCls,r=e.iconCls,c=e.antCls,a=e.zIndexPopup,l=e.colorText,i=e.colorWarning,s=e.marginXXS,u=e.marginXS,d=e.fontSize,p=e.fontWeightStrong,f=e.colorTextHeading;return(0,Z.Z)({},t,(o={zIndex:a},(0,Z.Z)(o,"&".concat(c,"-popover"),{fontSize:d}),(0,Z.Z)(o,"".concat(t,"-message"),(n={marginBottom:u,display:"flex",flexWrap:"nowrap",alignItems:"start"},(0,Z.Z)(n,"> ".concat(t,"-message-icon ").concat(r),{color:i,fontSize:d,lineHeight:1,marginInlineEnd:u}),(0,Z.Z)(n,"".concat(t,"-title"),{fontWeight:p,color:f,"&:only-child":{fontWeight:"normal"}}),(0,Z.Z)(n,"".concat(t,"-description"),{marginTop:s,color:l}),n)),(0,Z.Z)(o,"".concat(t,"-buttons"),{textAlign:"end",whiteSpace:"nowrap",button:{marginInlineStart:u}}),o))}(e)}),(function(e){return{zIndexPopup:e.zIndexPopupBase+60}})),k=function(e,n){var o={};for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&n.indexOf(t)<0&&(o[t]=e[t]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(t=Object.getOwnPropertySymbols(e);r<t.length;r++)n.indexOf(t[r])<0&&Object.prototype.propertyIsEnumerable.call(e,t[r])&&(o[t[r]]=e[t[r]])}return o},S=function(e){var n=e.prefixCls,o=e.okButtonProps,c=e.cancelButtonProps,l=e.title,i=e.description,s=e.cancelText,d=e.okText,f=e.okType,h=void 0===f?"primary":f,Z=e.icon,x=void 0===Z?u.createElement(r.Z,null):Z,O=e.showCancel,k=void 0===O||O,S=e.close,E=e.onConfirm,P=e.onCancel,j=e.onPopupClick,w=u.useContext(p.E_).getPrefixCls,N=(0,C.Z)("Popconfirm",y.Z.Popconfirm),T=(0,t.Z)(N,1)[0],I=(0,m.Z)(l),z=(0,m.Z)(i);return u.createElement("div",{className:"".concat(n,"-inner-content"),onClick:j},u.createElement("div",{className:"".concat(n,"-message")},x&&u.createElement("span",{className:"".concat(n,"-message-icon")},x),u.createElement("div",{className:"".concat(n,"-message-text")},I&&u.createElement("div",{className:a()("".concat(n,"-title"))},I),z&&u.createElement("div",{className:"".concat(n,"-description")},z))),u.createElement("div",{className:"".concat(n,"-buttons")},k&&u.createElement(v.ZP,Object.assign({onClick:P,size:"small"},c),null!==s&&void 0!==s?s:null===T||void 0===T?void 0:T.cancelText),u.createElement(g.Z,{buttonProps:Object.assign(Object.assign({size:"small"},(0,b.n)(h)),o),actionFn:E,close:S,prefixCls:w("btn"),quitOnNullishReturnValue:!0,emitEvent:!0},null!==d&&void 0!==d?d:null===T||void 0===T?void 0:T.okText)))},E=function(e){var n=e.prefixCls,o=e.placement,r=e.className,c=e.style,l=k(e,["prefixCls","placement","className","style"]),i=(0,u.useContext(p.E_).getPrefixCls)("popconfirm",n),s=O(i);return(0,(0,t.Z)(s,1)[0])(u.createElement(h.ZP,{placement:o,className:a()(i,r),style:c,content:u.createElement(S,Object.assign({prefixCls:i},l))}))},P=void 0,j=function(e,n){var o={};for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&n.indexOf(t)<0&&(o[t]=e[t]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(t=Object.getOwnPropertySymbols(e);r<t.length;r++)n.indexOf(t[r])<0&&Object.prototype.propertyIsEnumerable.call(e,t[r])&&(o[t[r]]=e[t[r]])}return o},w=u.forwardRef((function(e,n){var o=e.prefixCls,c=e.placement,g=void 0===c?"top":c,m=e.trigger,v=void 0===m?"click":m,b=e.okType,C=void 0===b?"primary":b,y=e.icon,h=void 0===y?u.createElement(r.Z,null):y,Z=e.children,x=e.overlayClassName,k=e.onOpenChange,E=e.onVisibleChange,w=j(e,["prefixCls","placement","trigger","okType","icon","children","overlayClassName","onOpenChange","onVisibleChange"]),N=u.useContext(p.E_).getPrefixCls,T=(0,i.Z)(!1,{value:e.open,defaultValue:e.defaultOpen}),I=(0,t.Z)(T,2),z=I[0],B=I[1],_=function(e,n){B(e,!0),null===E||void 0===E||E(e),null===k||void 0===k||k(e,n)},H=N("popconfirm",o),W=a()(H,x),L=O(H);return(0,(0,t.Z)(L,1)[0])(u.createElement(f.Z,Object.assign({},(0,s.Z)(w,["title"]),{trigger:v,placement:g,onOpenChange:function(n){var o=e.disabled;void 0!==o&&o||_(n)},open:z,ref:n,overlayClassName:W,content:u.createElement(S,Object.assign({okType:C,icon:h},e,{prefixCls:H,close:function(e){_(!1,e)},onConfirm:function(n){var o;return null===(o=e.onConfirm)||void 0===o?void 0:o.call(P,n)},onCancel:function(n){var o;_(!1,n),null===(o=e.onCancel)||void 0===o||o.call(P,n)}})),"data-popover-inject":!0}),(0,d.Tm)(Z,{onKeyDown:function(e){var n,o;u.isValidElement(Z)&&(null===(o=null===Z||void 0===Z?void 0:(n=Z.props).onKeyDown)||void 0===o||o.call(n,e)),function(e){e.keyCode===l.Z.ESC&&z&&_(!1,e)}(e)}})))}));w._InternalPanelDoNotUseOrYouWillBeFired=E;var N=w},5870:function(e,n,o){o.d(n,{Z:function(){return E}});var t=o(4942),r=o(9439),c=o(1662),a=o(3270),l=o.n(a),i=o(4519),s=o(1235),u=o(9869),d=o(9495),p=o(564);var f=o(1480),g=o(150),m=o(111),v=o(1157),b=function(e,n,o){var r,c="string"!==typeof(r=o)?r:r.charAt(0).toUpperCase()+r.slice(1);return(0,t.Z)({},"".concat(e.componentCls,"-").concat(n),(0,t.Z)({color:e["color".concat(o)],background:e["color".concat(c,"Bg")],borderColor:e["color".concat(c,"Border")]},"&".concat(e.componentCls,"-borderless"),{borderColor:"transparent"}))},C=function(e){return(0,g.Z)(e,(function(n,o){var r=o.textColor,c=o.lightBorderColor,a=o.lightColor,l=o.darkColor;return(0,t.Z)({},"".concat(e.componentCls,"-").concat(n),(0,t.Z)({color:r,background:a,borderColor:c,"&-inverse":{color:e.colorTextLightSolid,background:l,borderColor:l}},"&".concat(e.componentCls,"-borderless"),{borderColor:"transparent"}))}))},y=function(e){var n,o,r,c=e.paddingXXS,a=e.lineWidth,l=e.tagPaddingHorizontal,i=e.componentCls,s=l-a,u=c-a;return r={},(0,t.Z)(r,i,Object.assign(Object.assign({},(0,f.Wf)(e)),(o={display:"inline-block",height:"auto",marginInlineEnd:e.marginXS,paddingInline:s,fontSize:e.tagFontSize,lineHeight:e.tagLineHeight,whiteSpace:"nowrap",background:e.defaultBg,border:"".concat(e.lineWidth,"px ").concat(e.lineType," ").concat(e.colorBorder),borderRadius:e.borderRadiusSM,opacity:1,transition:"all ".concat(e.motionDurationMid),textAlign:"start",position:"relative"},(0,t.Z)(o,"&".concat(i,"-rtl"),{direction:"rtl"}),(0,t.Z)(o,"&, a, a:hover",{color:e.defaultColor}),(0,t.Z)(o,"".concat(i,"-close-icon"),{marginInlineStart:u,color:e.colorTextDescription,fontSize:e.tagIconSize,cursor:"pointer",transition:"all ".concat(e.motionDurationMid),"&:hover":{color:e.colorTextHeading}}),(0,t.Z)(o,"&".concat(i,"-has-color"),(0,t.Z)({borderColor:"transparent"},"&, a, a:hover, ".concat(e.iconCls,"-close, ").concat(e.iconCls,"-close:hover"),{color:e.colorTextLightSolid})),(0,t.Z)(o,"&-checkable",(n={backgroundColor:"transparent",borderColor:"transparent",cursor:"pointer"},(0,t.Z)(n,"&:not(".concat(i,"-checkable-checked):hover"),{color:e.colorPrimary,backgroundColor:e.colorFillSecondary}),(0,t.Z)(n,"&:active, &-checked",{color:e.colorTextLightSolid}),(0,t.Z)(n,"&-checked",{backgroundColor:e.colorPrimary,"&:hover":{backgroundColor:e.colorPrimaryHover}}),(0,t.Z)(n,"&:active",{backgroundColor:e.colorPrimaryActive}),n)),(0,t.Z)(o,"&-hidden",{display:"none"}),(0,t.Z)(o,"> ".concat(e.iconCls," + span, > span + ").concat(e.iconCls),{marginInlineStart:s}),o))),(0,t.Z)(r,"".concat(i,"-borderless"),{borderColor:"transparent",background:e.tagBorderlessBg}),r},h=(0,m.Z)("Tag",(function(e){var n=e.lineWidth,o=e.fontSizeIcon,t=e.fontSizeSM,r="".concat(e.lineHeightSM*t,"px"),c=(0,v.TS)(e,{tagFontSize:t,tagLineHeight:r,tagIconSize:o-2*n,tagPaddingHorizontal:8,tagBorderlessBg:e.colorFillTertiary});return[y(c),C(c),b(c,"success","Success"),b(c,"processing","Info"),b(c,"error","Error"),b(c,"warning","Warning")]}),(function(e){return{defaultBg:e.colorFillQuaternary,defaultColor:e.colorText}})),Z=function(e,n){var o={};for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&n.indexOf(t)<0&&(o[t]=e[t]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(t=Object.getOwnPropertySymbols(e);r<t.length;r++)n.indexOf(t[r])<0&&Object.prototype.propertyIsEnumerable.call(e,t[r])&&(o[t[r]]=e[t[r]])}return o},x=function(e){var n=e.prefixCls,o=e.className,c=e.checked,a=e.onChange,s=e.onClick,u=Z(e,["prefixCls","className","checked","onChange","onClick"]),d=(0,i.useContext(p.E_).getPrefixCls)("tag",n),f=h(d),g=(0,r.Z)(f,2),m=g[0],v=g[1],b=l()(d,"".concat(d,"-checkable"),(0,t.Z)({},"".concat(d,"-checkable-checked"),c),o,v);return m(i.createElement("span",Object.assign({},u,{className:b,onClick:function(e){null===a||void 0===a||a(!c),null===s||void 0===s||s(e)}})))},O=function(e,n){var o={};for(var t in e)Object.prototype.hasOwnProperty.call(e,t)&&n.indexOf(t)<0&&(o[t]=e[t]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(t=Object.getOwnPropertySymbols(e);r<t.length;r++)n.indexOf(t[r])<0&&Object.prototype.propertyIsEnumerable.call(e,t[r])&&(o[t[r]]=e[t[r]])}return o},k=function(e,n){var o,a=e.prefixCls,f=e.className,g=e.rootClassName,m=e.style,v=e.children,b=e.icon,C=e.color,y=e.onClose,Z=e.closeIcon,x=e.closable,k=e.bordered,S=void 0===k||k,E=O(e,["prefixCls","className","rootClassName","style","children","icon","color","onClose","closeIcon","closable","bordered"]),P=i.useContext(p.E_),j=P.getPrefixCls,w=P.direction,N=P.tag,T=i.useState(!0),I=(0,r.Z)(T,2),z=I[0],B=I[1];i.useEffect((function(){"visible"in E&&B(E.visible)}),[E.visible]);var _=(0,s.o2)(C)||(0,s.yT)(C),H=Object.assign(Object.assign({backgroundColor:C&&!_?C:void 0},null===N||void 0===N?void 0:N.style),m),W=j("tag",a),L=h(W),F=(0,r.Z)(L,2),M=F[0],R=F[1],D=l()(W,null===N||void 0===N?void 0:N.className,(o={},(0,t.Z)(o,"".concat(W,"-").concat(C),_),(0,t.Z)(o,"".concat(W,"-has-color"),C&&!_),(0,t.Z)(o,"".concat(W,"-hidden"),!z),(0,t.Z)(o,"".concat(W,"-rtl"),"rtl"===w),(0,t.Z)(o,"".concat(W,"-borderless"),!S),o),f,g,R),X=function(e){e.stopPropagation(),null===y||void 0===y||y(e),e.defaultPrevented||B(!1)},V=(0,u.Z)(x,Z,(function(e){return null===e?i.createElement(c.Z,{className:"".concat(W,"-close-icon"),onClick:X}):i.createElement("span",{className:"".concat(W,"-close-icon"),onClick:X},e)}),null,!1),A=(0,r.Z)(V,2)[1],K="function"===typeof E.onClick||v&&"a"===v.type,U=b||null,q=U?i.createElement(i.Fragment,null,U,v&&i.createElement("span",null,v)):v,Q=i.createElement("span",Object.assign({},E,{ref:n,className:D,style:H}),q,A);return M(K?i.createElement(d.Z,{component:"Tag"},Q):Q)},S=i.forwardRef(k);S.CheckableTag=x;var E=S}}]);
//# sourceMappingURL=978.707d31a2.chunk.js.map