"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[842],{9014:function(e,n,t){var o=t(9439),r=t(2792),a=t(4519),c=t(2513),i=t(2187);function l(e){return!(!e||!e.then)}n.Z=function(e){var n=e.type,t=e.children,s=e.prefixCls,d=e.buttonProps,u=e.close,f=e.autoFocus,m=e.emitEvent,p=e.isSilent,g=e.quitOnNullishReturnValue,v=e.actionFn,b=a.useRef(!1),C=a.useRef(null),y=(0,r.Z)(!1),x=(0,o.Z)(y,2),Z=x[0],h=x[1],S=function(){null===u||void 0===u||u.apply(void 0,arguments)};a.useEffect((function(){var e=null;return f&&(e=setTimeout((function(){var e;null===(e=C.current)||void 0===e||e.focus()}))),function(){e&&clearTimeout(e)}}),[]);return a.createElement(c.ZP,Object.assign({},(0,i.n)(n),{onClick:function(e){if(!b.current)if(b.current=!0,v){var n;if(m){if(n=v(e),g&&!l(n))return b.current=!1,void S(e)}else if(v.length)n=v(u),b.current=!1;else if(!(n=v()))return void S();!function(e){l(e)&&(h(!0),e.then((function(){h(!1,!0),S.apply(void 0,arguments),b.current=!1}),(function(e){if(h(!1,!0),b.current=!1,!(null===p||void 0===p?void 0:p()))return Promise.reject(e)})))}(n)}else S()},loading:Z,prefixCls:s},d,{ref:C}),t)}},9869:function(e,n,t){t.d(n,{Z:function(){return a}});var o=t(1662),r=t(4519);function a(e,n,t){var a=arguments.length>3&&void 0!==arguments[3]?arguments[3]:r.createElement(o.Z,null),c=function(e,n,t){return"boolean"===typeof e?e:void 0===n?!!t:!1!==n&&null!==n}(e,n,arguments.length>4&&void 0!==arguments[4]&&arguments[4]);if(!c)return[!1,null];var i="boolean"===typeof n||void 0===n||null===n?a:n;return[!0,t?t(i):i]}},3842:function(e,n,t){t.d(n,{Z:function(){return Me}});var o=t(3433),r=t(1277),a=t(4519),c=t(9002),i=t(4942),l=t(9439),s=t(4271),d=t(9434),u=t(8724),f=t(2181),m=t(3270),p=t.n(m),g=t(9014),v=t(7189),b=t(6951),C=t(1662),y=t(7462),x=t(6279),Z=t(1413),h=t(4621),S=t(1451),k=t(3714),O=t(3946);function E(e,n,t){var o=n;return!o&&t&&(o="".concat(e,"-").concat(t)),o}function w(e,n){var t=e["page".concat(n?"Y":"X","Offset")],o="scroll".concat(n?"Top":"Left");if("number"!==typeof t){var r=e.document;"number"!==typeof(t=r.documentElement[o])&&(t=r.body[o])}return t}var P=t(6114),N=a.memo((function(e){return e.children}),(function(e,n){return!n.shouldUpdate})),T={width:0,height:0,overflow:"hidden",outline:"none"},j=a.forwardRef((function(e,n){var t=e.prefixCls,o=e.className,r=e.style,c=e.title,i=e.ariaId,l=e.footer,s=e.closable,d=e.closeIcon,u=e.onClose,f=e.children,m=e.bodyStyle,g=e.bodyProps,v=e.modalRender,b=e.onMouseDown,C=e.onMouseUp,x=e.holderRef,h=e.visible,S=e.forceRender,k=e.width,O=e.height,E=(0,a.useRef)(),w=(0,a.useRef)();a.useImperativeHandle(n,(function(){return{focus:function(){var e;null===(e=E.current)||void 0===e||e.focus()},changeActive:function(e){var n=document.activeElement;e&&n===w.current?E.current.focus():e||n!==E.current||w.current.focus()}}}));var P,j,I,B={};void 0!==k&&(B.width=k),void 0!==O&&(B.height=O),l&&(P=a.createElement("div",{className:"".concat(t,"-footer")},l)),c&&(j=a.createElement("div",{className:"".concat(t,"-header")},a.createElement("div",{className:"".concat(t,"-title"),id:i},c))),s&&(I=a.createElement("button",{type:"button",onClick:u,"aria-label":"Close",className:"".concat(t,"-close")},d||a.createElement("span",{className:"".concat(t,"-close-x")})));var z=a.createElement("div",{className:"".concat(t,"-content")},I,j,a.createElement("div",(0,y.Z)({className:"".concat(t,"-body"),style:m},g),f),P);return a.createElement("div",{key:"dialog-element",role:"dialog","aria-labelledby":c?i:null,"aria-modal":"true",ref:x,style:(0,Z.Z)((0,Z.Z)({},r),B),className:p()(t,o),onMouseDown:b,onMouseUp:C},a.createElement("div",{tabIndex:0,ref:E,style:T,"aria-hidden":"true"}),a.createElement(N,{shouldUpdate:h||S},v?v(z):z),a.createElement("div",{tabIndex:0,ref:w,style:T,"aria-hidden":"true"}))}));var I=j,B=a.forwardRef((function(e,n){var t=e.prefixCls,o=e.title,r=e.style,c=e.className,i=e.visible,s=e.forceRender,d=e.destroyOnClose,u=e.motionName,f=e.ariaId,m=e.onVisibleChanged,g=e.mousePosition,v=(0,a.useRef)(),b=a.useState(),C=(0,l.Z)(b,2),x=C[0],h=C[1],S={};function k(){var e=function(e){var n=e.getBoundingClientRect(),t={left:n.left,top:n.top},o=e.ownerDocument,r=o.defaultView||o.parentWindow;return t.left+=w(r),t.top+=w(r,!0),t}(v.current);h(g?"".concat(g.x-e.left,"px ").concat(g.y-e.top,"px"):"")}return x&&(S.transformOrigin=x),a.createElement(P.ZP,{visible:i,onVisibleChanged:m,onAppearPrepare:k,onEnterPrepare:k,forceRender:s,motionName:u,removeOnLeave:d,ref:v},(function(i,l){var s=i.className,d=i.style;return a.createElement(I,(0,y.Z)({},e,{ref:n,title:o,ariaId:f,prefixCls:t,holderRef:l,style:(0,Z.Z)((0,Z.Z)((0,Z.Z)({},d),r),S),className:p()(c,s)}))}))}));B.displayName="Content";var z=B;function H(e){var n=e.prefixCls,t=e.style,o=e.visible,r=e.maskProps,c=e.motionName;return a.createElement(P.ZP,{key:"mask",visible:o,motionName:c,leavedClassName:"".concat(n,"-mask-hidden")},(function(e,o){var c=e.className,i=e.style;return a.createElement("div",(0,y.Z)({ref:o,style:(0,Z.Z)((0,Z.Z)({},i),t),className:p()("".concat(n,"-mask"),c)},r))}))}function R(e){var n=e.prefixCls,t=void 0===n?"rc-dialog":n,o=e.zIndex,r=e.visible,c=void 0!==r&&r,i=e.keyboard,s=void 0===i||i,d=e.focusTriggerAfterClose,u=void 0===d||d,f=e.wrapStyle,m=e.wrapClassName,g=e.wrapProps,v=e.onClose,b=e.afterOpenChange,C=e.afterClose,x=e.transitionName,w=e.animation,P=e.closable,N=void 0===P||P,T=e.mask,j=void 0===T||T,I=e.maskTransitionName,B=e.maskAnimation,R=e.maskClosable,F=void 0===R||R,M=e.maskStyle,W=e.maskProps,A=e.rootClassName,D=(0,a.useRef)(),L=(0,a.useRef)(),G=(0,a.useRef)(),_=a.useState(c),X=(0,l.Z)(_,2),U=X[0],V=X[1],Y=(0,S.Z)();function K(e){null===v||void 0===v||v(e)}var q=(0,a.useRef)(!1),Q=(0,a.useRef)(),J=null;return F&&(J=function(e){q.current?q.current=!1:L.current===e.target&&K(e)}),(0,a.useEffect)((function(){c&&(V(!0),(0,h.Z)(L.current,document.activeElement)||(D.current=document.activeElement))}),[c]),(0,a.useEffect)((function(){return function(){clearTimeout(Q.current)}}),[]),a.createElement("div",(0,y.Z)({className:p()("".concat(t,"-root"),A)},(0,O.Z)(e,{data:!0})),a.createElement(H,{prefixCls:t,visible:j&&c,motionName:E(t,I,B),style:(0,Z.Z)({zIndex:o},M),maskProps:W}),a.createElement("div",(0,y.Z)({tabIndex:-1,onKeyDown:function(e){if(s&&e.keyCode===k.Z.ESC)return e.stopPropagation(),void K(e);c&&e.keyCode===k.Z.TAB&&G.current.changeActive(!e.shiftKey)},className:p()("".concat(t,"-wrap"),m),ref:L,onClick:J,style:(0,Z.Z)((0,Z.Z)({zIndex:o},f),{},{display:U?null:"none"})},g),a.createElement(z,(0,y.Z)({},e,{onMouseDown:function(){clearTimeout(Q.current),q.current=!0},onMouseUp:function(){Q.current=setTimeout((function(){q.current=!1}))},ref:G,closable:N,ariaId:Y,prefixCls:t,visible:c&&U,onClose:K,onVisibleChanged:function(e){if(e)!function(){var e;(0,h.Z)(L.current,document.activeElement)||null===(e=G.current)||void 0===e||e.focus()}();else{if(V(!1),j&&D.current&&u){try{D.current.focus({preventScroll:!0})}catch(n){}D.current=null}U&&(null===C||void 0===C||C())}null===b||void 0===b||b(e)},motionName:E(t,x,w)}))))}var F=function(e){var n=e.visible,t=e.getContainer,o=e.forceRender,r=e.destroyOnClose,c=void 0!==r&&r,i=e.afterClose,s=a.useState(n),d=(0,l.Z)(s,2),u=d[0],f=d[1];return a.useEffect((function(){n&&f(!0)}),[n]),o||!c||u?a.createElement(x.Z,{open:n||o||u,autoDestroy:!1,getContainer:t,autoLock:n||u},a.createElement(R,(0,y.Z)({},e,{destroyOnClose:c,afterClose:function(){null===i||void 0===i||i(),f(!1)}}))):null};F.displayName="Dialog";var M=F,W=t(9869),A=t(5706),D=t(564),L=t(4412),G=t(2746),_=t(2513),X=t(2187),U=t(6963),V=t(7147);function Y(e,n){return a.createElement("span",{className:"".concat(e,"-close-x")},n||a.createElement(C.Z,{className:"".concat(e,"-close-icon")}))}var K=function(e){var n=e.okText,t=e.okType,o=void 0===t?"primary":t,r=e.cancelText,c=e.confirmLoading,i=e.onOk,s=e.onCancel,d=e.okButtonProps,u=e.cancelButtonProps,f=(0,b.Z)("Modal",(0,V.A)()),m=(0,l.Z)(f,1)[0];return a.createElement(U.n,{disabled:!1},a.createElement(_.ZP,Object.assign({onClick:s},u),r||(null===m||void 0===m?void 0:m.cancelText)),a.createElement(_.ZP,Object.assign({},(0,X.n)(o),{loading:c,onClick:i},d),n||(null===m||void 0===m?void 0:m.okText)))},q=t(1480),Q=t(7340),J=t(9103),$=new Q.E4("antFadeIn",{"0%":{opacity:0},"100%":{opacity:1}}),ee=new Q.E4("antFadeOut",{"0%":{opacity:1},"100%":{opacity:0}}),ne=function(e){var n,t=arguments.length>1&&void 0!==arguments[1]&&arguments[1],o=e.antCls,r="".concat(o,"-fade"),a=t?"&":"";return[(0,J.R)(r,$,ee,e.motionDurationMid,t),(n={},(0,i.Z)(n,"\n        ".concat(a).concat(r,"-enter,\n        ").concat(a).concat(r,"-appear\n      "),{opacity:0,animationTimingFunction:"linear"}),(0,i.Z)(n,"".concat(a).concat(r,"-leave"),{animationTimingFunction:"linear"}),n)]},te=t(9287),oe=t(111),re=t(1157);function ae(e){return{position:e,top:0,insetInlineEnd:0,bottom:0,insetInlineStart:0}}var ce,ie=function(e){var n,t=e.componentCls,o=e.antCls;return[(0,i.Z)({},"".concat(t,"-root"),(n={},(0,i.Z)(n,"".concat(t).concat(o,"-zoom-enter, ").concat(t).concat(o,"-zoom-appear"),{transform:"none",opacity:0,animationDuration:e.motionDurationSlow,userSelect:"none"}),(0,i.Z)(n,"".concat(t).concat(o,"-zoom-leave ").concat(t,"-content"),{pointerEvents:"none"}),(0,i.Z)(n,"".concat(t,"-mask"),Object.assign(Object.assign({},ae("fixed")),(0,i.Z)({zIndex:e.zIndexPopupBase,height:"100%",backgroundColor:e.colorBgMask},"".concat(t,"-hidden"),{display:"none"}))),(0,i.Z)(n,"".concat(t,"-wrap"),Object.assign(Object.assign({},ae("fixed")),{overflow:"auto",outline:0,WebkitOverflowScrolling:"touch"})),n)),(0,i.Z)({},"".concat(t,"-root"),ne(e))]},le=function(e){var n,t,o,r,a=e.componentCls;return[(0,i.Z)({},"".concat(a,"-root"),(t={},(0,i.Z)(t,"".concat(a,"-wrap"),{zIndex:e.zIndexPopupBase,position:"fixed",inset:0,overflow:"auto",outline:0,WebkitOverflowScrolling:"touch"}),(0,i.Z)(t,"".concat(a,"-wrap-rtl"),{direction:"rtl"}),(0,i.Z)(t,"".concat(a,"-centered"),(0,i.Z)({textAlign:"center","&::before":{display:"inline-block",width:0,height:"100%",verticalAlign:"middle",content:'""'}},a,{top:0,display:"inline-block",paddingBottom:0,textAlign:"start",verticalAlign:"middle"})),(0,i.Z)(t,"@media (max-width: ".concat(e.screenSMMax,")"),(n={},(0,i.Z)(n,a,{maxWidth:"calc(100vw - 16px)",margin:"".concat(e.marginXS," auto")}),(0,i.Z)(n,"".concat(a,"-centered"),(0,i.Z)({},a,{flex:1})),n)),t)),(0,i.Z)({},a,Object.assign(Object.assign({},(0,q.Wf)(e)),(o={pointerEvents:"none",position:"relative",top:100,width:"auto",maxWidth:"calc(100vw - ".concat(2*e.margin,"px)"),margin:"0 auto",paddingBottom:e.paddingLG},(0,i.Z)(o,"".concat(a,"-title"),{margin:0,color:e.titleColor,fontWeight:e.fontWeightStrong,fontSize:e.titleFontSize,lineHeight:e.titleLineHeight,wordWrap:"break-word"}),(0,i.Z)(o,"".concat(a,"-content"),{position:"relative",backgroundColor:e.contentBg,backgroundClip:"padding-box",border:0,borderRadius:e.borderRadiusLG,boxShadow:e.boxShadow,pointerEvents:"auto",padding:"".concat(e.paddingMD,"px ").concat(e.paddingContentHorizontalLG,"px")}),(0,i.Z)(o,"".concat(a,"-close"),Object.assign({position:"absolute",top:(e.modalHeaderHeight-e.modalCloseBtnSize)/2,insetInlineEnd:(e.modalHeaderHeight-e.modalCloseBtnSize)/2,zIndex:e.zIndexPopupBase+10,padding:0,color:e.modalCloseIconColor,fontWeight:e.fontWeightStrong,lineHeight:1,textDecoration:"none",background:"transparent",borderRadius:e.borderRadiusSM,width:e.modalCloseBtnSize,height:e.modalCloseBtnSize,border:0,outline:0,cursor:"pointer",transition:"color ".concat(e.motionDurationMid,", background-color ").concat(e.motionDurationMid),"&-x":{display:"flex",fontSize:e.fontSizeLG,fontStyle:"normal",lineHeight:"".concat(e.modalCloseBtnSize,"px"),justifyContent:"center",textTransform:"none",textRendering:"auto"},"&:hover":{color:e.modalIconHoverColor,backgroundColor:e.wireframe?"transparent":e.colorFillContent,textDecoration:"none"},"&:active":{backgroundColor:e.wireframe?"transparent":e.colorFillContentHover}},(0,q.Qy)(e))),(0,i.Z)(o,"".concat(a,"-header"),{color:e.colorText,background:e.headerBg,borderRadius:"".concat(e.borderRadiusLG,"px ").concat(e.borderRadiusLG,"px 0 0"),marginBottom:e.marginXS}),(0,i.Z)(o,"".concat(a,"-body"),{fontSize:e.fontSize,lineHeight:e.lineHeight,wordWrap:"break-word"}),(0,i.Z)(o,"".concat(a,"-footer"),(0,i.Z)({textAlign:"end",background:e.footerBg,marginTop:e.marginSM},"".concat(e.antCls,"-btn + ").concat(e.antCls,"-btn:not(").concat(e.antCls,"-dropdown-trigger)"),{marginBottom:0,marginInlineStart:e.marginXS})),(0,i.Z)(o,"".concat(a,"-open"),{overflow:"hidden"}),o))),(0,i.Z)({},"".concat(a,"-pure-panel"),(r={top:"auto",padding:0,display:"flex",flexDirection:"column"},(0,i.Z)(r,"".concat(a,"-content,\n          ").concat(a,"-body,\n          ").concat(a,"-confirm-body-wrapper"),{display:"flex",flexDirection:"column",flex:"auto"}),(0,i.Z)(r,"".concat(a,"-confirm-body"),{marginBottom:"auto"}),r))]},se=function(e){var n,t,o,r,a=e.componentCls,c="".concat(a,"-confirm");return r={},(0,i.Z)(r,c,(o={"&-rtl":{direction:"rtl"}},(0,i.Z)(o,"".concat(e.antCls,"-modal-header"),{display:"none"}),(0,i.Z)(o,"".concat(c,"-body-wrapper"),Object.assign({},(0,q.dF)())),(0,i.Z)(o,"".concat(c,"-body"),(t={display:"flex",flexWrap:"wrap",alignItems:"center"},(0,i.Z)(t,"".concat(c,"-title"),(0,i.Z)({flex:"0 0 100%",display:"block",overflow:"hidden",color:e.colorTextHeading,fontWeight:e.fontWeightStrong,fontSize:e.titleFontSize,lineHeight:e.titleLineHeight},"+ ".concat(c,"-content"),{marginBlockStart:e.marginXS,flexBasis:"100%",maxWidth:"calc(100% - ".concat(e.modalConfirmIconSize+e.marginSM,"px)")})),(0,i.Z)(t,"".concat(c,"-content"),{color:e.colorText,fontSize:e.fontSize}),(0,i.Z)(t,"> ".concat(e.iconCls),(n={flex:"none",marginInlineEnd:e.marginSM,fontSize:e.modalConfirmIconSize},(0,i.Z)(n,"+ ".concat(c,"-title"),{flex:1}),(0,i.Z)(n,"+ ".concat(c,"-title + ").concat(c,"-content"),{marginInlineStart:e.modalConfirmIconSize+e.marginSM}),n)),t)),(0,i.Z)(o,"".concat(c,"-btns"),(0,i.Z)({textAlign:"end",marginTop:e.marginSM},"".concat(e.antCls,"-btn + ").concat(e.antCls,"-btn"),{marginBottom:0,marginInlineStart:e.marginXS})),o)),(0,i.Z)(r,"".concat(c,"-error ").concat(c,"-body > ").concat(e.iconCls),{color:e.colorError}),(0,i.Z)(r,"".concat(c,"-warning ").concat(c,"-body > ").concat(e.iconCls,",\n        ").concat(c,"-confirm ").concat(c,"-body > ").concat(e.iconCls),{color:e.colorWarning}),(0,i.Z)(r,"".concat(c,"-info ").concat(c,"-body > ").concat(e.iconCls),{color:e.colorInfo}),(0,i.Z)(r,"".concat(c,"-success ").concat(c,"-body > ").concat(e.iconCls),{color:e.colorSuccess}),r},de=function(e){var n=e.componentCls;return(0,i.Z)({},"".concat(n,"-root"),(0,i.Z)({},"".concat(n,"-wrap-rtl"),(0,i.Z)({direction:"rtl"},"".concat(n,"-confirm-body"),{direction:"rtl"})))},ue=function(e){var n,t,o,r=e.componentCls,a=e.antCls,c="".concat(r,"-confirm");return o={},(0,i.Z)(o,r,(n={},(0,i.Z)(n,"".concat(r,"-content"),{padding:0}),(0,i.Z)(n,"".concat(r,"-header"),{padding:e.modalHeaderPadding,borderBottom:"".concat(e.modalHeaderBorderWidth,"px ").concat(e.modalHeaderBorderStyle," ").concat(e.modalHeaderBorderColorSplit),marginBottom:0}),(0,i.Z)(n,"".concat(r,"-body"),{padding:e.modalBodyPadding}),(0,i.Z)(n,"".concat(r,"-footer"),{padding:"".concat(e.modalFooterPaddingVertical,"px ").concat(e.modalFooterPaddingHorizontal,"px"),borderTop:"".concat(e.modalFooterBorderWidth,"px ").concat(e.modalFooterBorderStyle," ").concat(e.modalFooterBorderColorSplit),borderRadius:"0 0 ".concat(e.borderRadiusLG,"px ").concat(e.borderRadiusLG,"px"),marginTop:0}),n)),(0,i.Z)(o,c,(t={},(0,i.Z)(t,"".concat(a,"-modal-body"),{padding:"".concat(2*e.padding,"px ").concat(2*e.padding,"px ").concat(e.paddingLG,"px")}),(0,i.Z)(t,"".concat(c,"-body"),(0,i.Z)({},"> ".concat(e.iconCls),(0,i.Z)({marginInlineEnd:e.margin},"+ ".concat(c,"-title + ").concat(c,"-content"),{marginInlineStart:e.modalConfirmIconSize+e.margin}))),(0,i.Z)(t,"".concat(c,"-btns"),{marginTop:e.marginLG}),t)),o},fe=(0,oe.Z)("Modal",(function(e){var n=e.padding,t=e.fontSizeHeading5,o=e.lineHeightHeading5,r=(0,re.TS)(e,{modalBodyPadding:e.paddingLG,modalHeaderPadding:"".concat(n,"px ").concat(e.paddingLG,"px"),modalHeaderBorderWidth:e.lineWidth,modalHeaderBorderStyle:e.lineType,modalHeaderBorderColorSplit:e.colorSplit,modalHeaderHeight:o*t+2*n,modalFooterBorderColorSplit:e.colorSplit,modalFooterBorderStyle:e.lineType,modalFooterPaddingVertical:e.paddingXS,modalFooterPaddingHorizontal:e.padding,modalFooterBorderWidth:e.lineWidth,modalIconHoverColor:e.colorIconHover,modalCloseIconColor:e.colorIcon,modalCloseBtnSize:e.fontSize*e.lineHeight,modalConfirmIconSize:e.fontSize*e.lineHeight});return[le(r),se(r),de(r),ie(r),e.wireframe&&ue(r),(0,te._y)(r,"zoom")]}),(function(e){return{footerBg:"transparent",headerBg:e.colorBgElevated,titleLineHeight:e.lineHeightHeading5,titleFontSize:e.fontSizeHeading5,contentBg:e.colorBgElevated,titleColor:e.colorTextHeading}})),me=function(e,n){var t={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&n.indexOf(o)<0&&(t[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)n.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(t[o[r]]=e[o[r]])}return t};(0,A.jD)()&&document.documentElement.addEventListener("click",(function(e){ce={x:e.pageX,y:e.pageY},setTimeout((function(){ce=null}),100)}),!0);var pe=function(e){var n,t,o=a.useContext(D.E_),r=o.getPopupContainer,c=o.getPrefixCls,s=o.direction,d=o.modal,u=function(n){var t=e.onCancel;null===t||void 0===t||t(n)},f=e.prefixCls,m=e.className,g=e.rootClassName,b=e.open,y=e.wrapClassName,x=e.centered,Z=e.getContainer,h=e.closeIcon,S=e.closable,k=e.focusTriggerAfterClose,O=void 0===k||k,E=e.style,w=e.visible,P=e.width,N=void 0===P?520:P,T=e.footer,j=me(e,["prefixCls","className","rootClassName","open","wrapClassName","centered","getContainer","closeIcon","closable","focusTriggerAfterClose","style","visible","width","footer"]),I=c("modal",f),B=c(),z=fe(I),H=(0,l.Z)(z,2),R=H[0],F=H[1],A=p()(y,(n={},(0,i.Z)(n,"".concat(I,"-centered"),!!x),(0,i.Z)(n,"".concat(I,"-wrap-rtl"),"rtl"===s),n));var _=void 0===T?a.createElement(K,Object.assign({},e,{onOk:function(n){var t=e.onOk;null===t||void 0===t||t(n)},onCancel:u})):T,X=(0,W.Z)(S,h,(function(e){return Y(I,e)}),a.createElement(C.Z,{className:"".concat(I,"-close-icon")}),!0),U=(0,l.Z)(X,2),V=U[0],q=U[1];return R(a.createElement(G.BR,null,a.createElement(L.Ux,{status:!0,override:!0},a.createElement(M,Object.assign({width:N},j,{getContainer:void 0===Z?r:Z,prefixCls:I,rootClassName:p()(F,g),wrapClassName:A,footer:_,visible:null!==b&&void 0!==b?b:w,mousePosition:null!==(t=j.mousePosition)&&void 0!==t?t:ce,onClose:u,closable:V,closeIcon:q,focusTriggerAfterClose:O,transitionName:(0,v.m)(B,"zoom",e.transitionName),maskTransitionName:(0,v.m)(B,"fade",e.maskTransitionName),className:p()(F,m,null===d||void 0===d?void 0:d.className),style:Object.assign(Object.assign({},null===d||void 0===d?void 0:d.style),E)})))))};function ge(e){var n=e.icon,t=e.onCancel,o=e.onOk,r=e.close,c=e.onConfirm,i=e.isSilent,m=e.okText,p=e.okButtonProps,v=e.cancelText,C=e.cancelButtonProps,y=e.confirmPrefixCls,x=e.rootPrefixCls,Z=e.type,h=e.okCancel,S=e.footer,k=e.locale,O=n;if(!n&&null!==n)switch(Z){case"info":O=a.createElement(f.Z,null);break;case"success":O=a.createElement(s.Z,null);break;case"error":O=a.createElement(d.Z,null);break;default:O=a.createElement(u.Z,null)}var E=e.okType||"primary",w=null!==h&&void 0!==h?h:"confirm"===Z,P=null!==e.autoFocusButton&&(e.autoFocusButton||"ok"),N=(0,b.Z)("Modal"),T=(0,l.Z)(N,1)[0],j=k||T,I=w&&a.createElement(g.Z,{isSilent:i,actionFn:t,close:function(){null===r||void 0===r||r.apply(void 0,arguments),null===c||void 0===c||c(!1)},autoFocus:"cancel"===P,buttonProps:C,prefixCls:"".concat(x,"-btn")},v||(null===j||void 0===j?void 0:j.cancelText));return a.createElement("div",{className:"".concat(y,"-body-wrapper")},a.createElement("div",{className:"".concat(y,"-body")},O,void 0===e.title?null:a.createElement("span",{className:"".concat(y,"-title")},e.title),a.createElement("div",{className:"".concat(y,"-content")},e.content)),void 0===S?a.createElement("div",{className:"".concat(y,"-btns")},I,a.createElement(g.Z,{isSilent:i,type:E,actionFn:o,close:function(){null===r||void 0===r||r.apply(void 0,arguments),null===c||void 0===c||c(!0)},autoFocus:"ok"===P,buttonProps:p,prefixCls:"".concat(x,"-btn")},m||(w?null===j||void 0===j?void 0:j.okText:null===j||void 0===j?void 0:j.justOkText))):S)}var ve=function(e){var n=e.close,t=e.zIndex,o=e.afterClose,r=(e.visible,e.open),l=e.keyboard,s=e.centered,d=e.getContainer,u=e.maskStyle,f=e.direction,m=e.prefixCls,g=e.wrapClassName,b=e.rootPrefixCls,C=e.iconPrefixCls,y=e.theme,x=e.bodyStyle,Z=e.closable,h=void 0!==Z&&Z,S=e.closeIcon,k=e.modalRender,O=e.focusTriggerAfterClose;var E="".concat(m,"-confirm"),w=e.width||416,P=e.style||{},N=void 0===e.mask||e.mask,T=void 0!==e.maskClosable&&e.maskClosable,j=p()(E,"".concat(E,"-").concat(e.type),(0,i.Z)({},"".concat(E,"-rtl"),"rtl"===f),e.className);return a.createElement(c.ZP,{prefixCls:b,iconPrefixCls:C,direction:f,theme:y},a.createElement(pe,{prefixCls:m,className:j,wrapClassName:p()((0,i.Z)({},"".concat(E,"-centered"),!!e.centered),g),onCancel:function(){return null===n||void 0===n?void 0:n({triggerCancel:!0})},open:r,title:"",footer:null,transitionName:(0,v.m)(b,"zoom",e.transitionName),maskTransitionName:(0,v.m)(b,"fade",e.maskTransitionName),mask:N,maskClosable:T,maskStyle:u,style:P,bodyStyle:x,width:w,zIndex:t,afterClose:o,keyboard:l,centered:s,getContainer:d,closable:h,closeIcon:S,modalRender:k,focusTriggerAfterClose:O},a.createElement(ge,Object.assign({},e,{confirmPrefixCls:E}))))},be=[],Ce=function(e,n){var t={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&n.indexOf(o)<0&&(t[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)n.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(t[o[r]]=e[o[r]])}return t},ye="";function xe(e){var n,t=document.createDocumentFragment(),i=Object.assign(Object.assign({},e),{close:d,open:!0});function l(){for(var n=arguments.length,a=new Array(n),c=0;c<n;c++)a[c]=arguments[c];var i=a.some((function(e){return e&&e.triggerCancel}));e.onCancel&&i&&e.onCancel.apply(e,[function(){}].concat((0,o.Z)(a.slice(1))));for(var l=0;l<be.length;l++){if(be[l]===d){be.splice(l,1);break}}(0,r.v)(t)}function s(e){var o=e.okText,i=e.cancelText,l=e.prefixCls,s=e.getContainer,d=Ce(e,["okText","cancelText","prefixCls","getContainer"]);clearTimeout(n),n=setTimeout((function(){var e=(0,V.A)(),n=(0,c.w6)(),u=n.getPrefixCls,f=n.getIconPrefixCls,m=n.getTheme,p=u(void 0,ye),g=l||"".concat(p,"-modal"),v=f(),b=m(),C=s;!1===C&&(C=void 0),(0,r.s)(a.createElement(ve,Object.assign({},d,{getContainer:C,prefixCls:g,rootPrefixCls:p,iconPrefixCls:v,okText:o,locale:e,theme:b,cancelText:i||e.cancelText})),t)}))}function d(){for(var n=this,t=arguments.length,o=new Array(t),r=0;r<t;r++)o[r]=arguments[r];(i=Object.assign(Object.assign({},i),{open:!1,afterClose:function(){"function"===typeof e.afterClose&&e.afterClose(),l.apply(n,o)}})).visible&&delete i.visible,s(i)}return s(i),be.push(d),{destroy:d,update:function(e){s(i="function"===typeof e?e(i):Object.assign(Object.assign({},i),e))}}}function Ze(e){return Object.assign(Object.assign({},e),{type:"warning"})}function he(e){return Object.assign(Object.assign({},e),{type:"info"})}function Se(e){return Object.assign(Object.assign({},e),{type:"success"})}function ke(e){return Object.assign(Object.assign({},e),{type:"error"})}function Oe(e){return Object.assign(Object.assign({},e),{type:"confirm"})}var Ee=t(516),we=function(e,n){var t={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&n.indexOf(o)<0&&(t[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)n.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(t[o[r]]=e[o[r]])}return t},Pe=(0,Ee.i)((function(e){var n=e.prefixCls,t=e.className,o=e.closeIcon,r=e.closable,c=e.type,i=e.title,s=e.children,d=we(e,["prefixCls","className","closeIcon","closable","type","title","children"]),u=a.useContext(D.E_).getPrefixCls,f=u(),m=n||u("modal"),g=fe(m),v=(0,l.Z)(g,2)[1],b="".concat(m,"-confirm"),C={};return C=c?{closable:null!==r&&void 0!==r&&r,title:"",footer:"",children:a.createElement(ge,Object.assign({},e,{confirmPrefixCls:b,rootPrefixCls:f,content:s}))}:{closable:null===r||void 0===r||r,title:i,footer:void 0===e.footer?a.createElement(K,Object.assign({},e)):e.footer,children:s},a.createElement(I,Object.assign({prefixCls:m,className:p()(v,"".concat(m,"-pure-panel"),c&&b,c&&"".concat(b,"-").concat(c),t)},d,{closeIcon:Y(m,o),closable:r},C))}));var Ne=t(8557),Te=function(e,n){var t={};for(var o in e)Object.prototype.hasOwnProperty.call(e,o)&&n.indexOf(o)<0&&(t[o]=e[o]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var r=0;for(o=Object.getOwnPropertySymbols(e);r<o.length;r++)n.indexOf(o[r])<0&&Object.prototype.propertyIsEnumerable.call(e,o[r])&&(t[o[r]]=e[o[r]])}return t},je=function(e,n){var t,r=e.afterClose,c=e.config,i=Te(e,["afterClose","config"]),s=a.useState(!0),d=(0,l.Z)(s,2),u=d[0],f=d[1],m=a.useState(c),p=(0,l.Z)(m,2),g=p[0],v=p[1],C=a.useContext(D.E_),y=C.direction,x=C.getPrefixCls,Z=x("modal"),h=x(),S=function(){f(!1);for(var e=arguments.length,n=new Array(e),t=0;t<e;t++)n[t]=arguments[t];var r=n.some((function(e){return e&&e.triggerCancel}));g.onCancel&&r&&g.onCancel.apply(g,[function(){}].concat((0,o.Z)(n.slice(1))))};a.useImperativeHandle(n,(function(){return{destroy:S,update:function(e){v((function(n){return Object.assign(Object.assign({},n),e)}))}}}));var k=null!==(t=g.okCancel)&&void 0!==t?t:"confirm"===g.type,O=(0,b.Z)("Modal",Ne.Z.Modal),E=(0,l.Z)(O,1)[0];return a.createElement(ve,Object.assign({prefixCls:Z,rootPrefixCls:h},g,{close:S,open:u,afterClose:function(){var e;r(),null===(e=g.afterClose)||void 0===e||e.call(g)},okText:g.okText||(k?null===E||void 0===E?void 0:E.okText:null===E||void 0===E?void 0:E.justOkText),direction:g.direction||y,cancelText:g.cancelText||(null===E||void 0===E?void 0:E.cancelText)},i))},Ie=a.forwardRef(je),Be=0,ze=a.memo(a.forwardRef((function(e,n){var t=function(){var e=a.useState([]),n=(0,l.Z)(e,2),t=n[0],r=n[1];return[t,a.useCallback((function(e){return r((function(n){return[].concat((0,o.Z)(n),[e])})),function(){r((function(n){return n.filter((function(n){return n!==e}))}))}}),[])]}(),r=(0,l.Z)(t,2),c=r[0],i=r[1];return a.useImperativeHandle(n,(function(){return{patchElement:i}}),[]),a.createElement(a.Fragment,null,c)})));var He=function(){var e=a.useRef(null),n=a.useState([]),t=(0,l.Z)(n,2),r=t[0],c=t[1];a.useEffect((function(){r.length&&((0,o.Z)(r).forEach((function(e){e()})),c([]))}),[r]);var i=a.useCallback((function(n){return function(t){var r;Be+=1;var i,l,s=a.createRef(),d=new Promise((function(e){i=e})),u=!1,f=a.createElement(Ie,{key:"modal-".concat(Be),config:n(t),ref:s,afterClose:function(){null===l||void 0===l||l()},isSilent:function(){return u},onConfirm:function(e){i(e)}});(l=null===(r=e.current)||void 0===r?void 0:r.patchElement(f))&&be.push(l);var m={destroy:function(){function e(){var e;null===(e=s.current)||void 0===e||e.destroy()}s.current?e():c((function(n){return[].concat((0,o.Z)(n),[e])}))},update:function(e){function n(){var n;null===(n=s.current)||void 0===n||n.update(e)}s.current?n():c((function(e){return[].concat((0,o.Z)(e),[n])}))},then:function(e){return u=!0,d.then(e)}};return m}}),[]);return[a.useMemo((function(){return{info:i(he),success:i(Se),error:i(ke),warning:i(Ze),confirm:i(Oe)}}),[]),a.createElement(ze,{key:"modal-holder",ref:e})]};function Re(e){return xe(Ze(e))}var Fe=pe;Fe.useModal=He,Fe.info=function(e){return xe(he(e))},Fe.success=function(e){return xe(Se(e))},Fe.error=function(e){return xe(ke(e))},Fe.warning=Re,Fe.warn=Re,Fe.confirm=function(e){return xe(Oe(e))},Fe.destroyAll=function(){for(;be.length;){var e=be.pop();e&&e()}},Fe.config=function(e){var n=e.rootPrefixCls;ye=n},Fe._InternalPanelDoNotUseOrYouWillBeFired=Pe;var Me=Fe}}]);
//# sourceMappingURL=842.416bb98b.chunk.js.map