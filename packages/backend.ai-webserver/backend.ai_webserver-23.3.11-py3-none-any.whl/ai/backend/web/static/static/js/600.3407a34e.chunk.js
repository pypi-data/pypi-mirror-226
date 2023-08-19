"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[600],{558:function(t,e,n){n.d(e,{Z:function(){return l}});var a=n(7462),o=n(4519),c={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"defs",attrs:{},children:[{tag:"style",attrs:{}}]},{tag:"path",attrs:{d:"M482 152h60q8 0 8 8v704q0 8-8 8h-60q-8 0-8-8V160q0-8 8-8z"}},{tag:"path",attrs:{d:"M176 474h672q8 0 8 8v60q0 8-8 8H176q-8 0-8-8v-60q0-8 8-8z"}}]},name:"plus",theme:"outlined"},r=n(9491),i=function(t,e){return o.createElement(r.Z,(0,a.Z)({},t,{ref:e,icon:c}))};var l=o.forwardRef(i)},7600:function(t,e,n){n.d(e,{Z:function(){return Pt}});var a=n(4942),o=n(9439),c=n(1662),r=n(8841),i=n(558),l=n(3270),d=n.n(l),s=n(7462),u=n(1413),p=n(1002),v=n(4925),f=n(4519),b=n(7612),m=n(269),h=n(4278),g=(0,f.createContext)(null),Z=f.forwardRef((function(t,e){var n=t.prefixCls,a=t.className,o=t.style,c=t.id,r=t.active,i=t.tabKey,l=t.children;return f.createElement("div",{id:c&&"".concat(c,"-panel-").concat(i),role:"tabpanel",tabIndex:r?0:-1,"aria-labelledby":c&&"".concat(c,"-tab-").concat(i),"aria-hidden":!r,style:o,className:d()(n,r&&"".concat(n,"-active"),a),ref:e},l)}));var k=Z,x=["key","forceRender","style","className"];function y(t){var e=t.id,n=t.activeKey,o=t.animated,c=t.tabPosition,r=t.destroyInactiveTabPane,i=f.useContext(g),l=i.prefixCls,p=i.tabs,b=o.tabPane,m="".concat(l,"-tabpane");return f.createElement("div",{className:d()("".concat(l,"-content-holder"))},f.createElement("div",{className:d()("".concat(l,"-content"),"".concat(l,"-content-").concat(c),(0,a.Z)({},"".concat(l,"-content-animated"),b))},p.map((function(t){var a=t.key,c=t.forceRender,i=t.style,l=t.className,p=(0,v.Z)(t,x),g=a===n;return f.createElement(h.ZP,(0,s.Z)({key:a,visible:g,forceRender:c,removeOnLeave:!!r,leavedClassName:"".concat(m,"-hidden")},o.tabPaneMotion),(function(t,n){var o=t.style,c=t.className;return f.createElement(k,(0,s.Z)({},p,{prefixCls:m,id:e,tabKey:a,animated:b,active:g,style:(0,u.Z)((0,u.Z)({},i),o),className:d()(l,c),ref:n}))}))}))))}var _=n(3433),w=n(1928),S=n(4586),C=n(2058),E=n(742),P={width:0,height:0,left:0,top:0};function R(t,e){var n=f.useRef(t),a=f.useState({}),c=(0,o.Z)(a,2)[1];return[n.current,function(t){var a="function"===typeof t?t(n.current):t;a!==n.current&&e(a,n.current),n.current=a,c({})}]}var T=.1,I=.01,L=20,N=Math.pow(.995,L);var M=n(7878);function B(t){var e=(0,f.useState)(0),n=(0,o.Z)(e,2),a=n[0],c=n[1],r=(0,f.useRef)(0),i=(0,f.useRef)();return i.current=t,(0,M.o)((function(){var t;null===(t=i.current)||void 0===t||t.call(i)}),[a]),function(){r.current===a&&(r.current+=1,c(r.current))}}var z={width:0,height:0,left:0,top:0,right:0};function O(t){var e;return t instanceof Map?(e={},t.forEach((function(t,n){e[n]=t}))):e=t,JSON.stringify(e)}var D="TABS_DQ";function j(t){return String(t).replace(/"/g,D)}function G(t,e,n,a){return!(!n||a||!1===t||void 0===t&&(!1===e||null===e))}function A(t,e){var n=t.prefixCls,a=t.editable,o=t.locale,c=t.style;return a&&!1!==a.showAdd?f.createElement("button",{ref:e,type:"button",className:"".concat(n,"-nav-add"),style:c,"aria-label":(null===o||void 0===o?void 0:o.addAriaLabel)||"Add tab",onClick:function(t){a.onEdit("add",{event:t})}},a.addIcon||"+"):null}var H=f.forwardRef(A);var W=f.forwardRef((function(t,e){var n,a=t.position,o=t.prefixCls,c=t.extra;if(!c)return null;var r={};return"object"!==(0,p.Z)(c)||f.isValidElement(c)?r.right=c:r=c,"right"===a&&(n=r.right),"left"===a&&(n=r.left),n?f.createElement("div",{className:"".concat(o,"-extra-content"),ref:e},n):null})),X=n(871),K=n(571),F=n(3714);function q(t,e){var n=t.prefixCls,c=t.id,r=t.tabs,i=t.locale,l=t.mobile,s=t.moreIcon,u=void 0===s?"More":s,p=t.moreTransitionName,v=t.style,b=t.className,m=t.editable,h=t.tabBarGutter,g=t.rtl,Z=t.removeAriaLabel,k=t.onTabClick,x=t.getPopupContainer,y=t.popupClassName,_=(0,f.useState)(!1),w=(0,o.Z)(_,2),S=w[0],C=w[1],E=(0,f.useState)(null),P=(0,o.Z)(E,2),R=P[0],T=P[1],I="".concat(c,"-more-popup"),L="".concat(n,"-dropdown"),N=null!==R?"".concat(I,"-").concat(R):null,M=null===i||void 0===i?void 0:i.dropdownAriaLabel;var B=f.createElement(K.ZP,{onClick:function(t){var e=t.key,n=t.domEvent;k(e,n),C(!1)},prefixCls:"".concat(L,"-menu"),id:I,tabIndex:-1,role:"listbox","aria-activedescendant":N,selectedKeys:[R],"aria-label":void 0!==M?M:"expanded dropdown"},r.map((function(t){var e=t.closable,n=t.disabled,a=t.closeIcon,o=t.key,r=t.label,i=G(e,a,m,n);return f.createElement(K.sN,{key:o,id:"".concat(I,"-").concat(o),role:"option","aria-controls":c&&"".concat(c,"-panel-").concat(o),disabled:n},f.createElement("span",null,r),i&&f.createElement("button",{type:"button","aria-label":Z||"remove",tabIndex:0,className:"".concat(L,"-menu-item-remove"),onClick:function(t){t.stopPropagation(),function(t,e){t.preventDefault(),t.stopPropagation(),m.onEdit("remove",{key:e,event:t})}(t,o)}},a||m.removeIcon||"\xd7"))})));function z(t){for(var e=r.filter((function(t){return!t.disabled})),n=e.findIndex((function(t){return t.key===R}))||0,a=e.length,o=0;o<a;o+=1){var c=e[n=(n+t+a)%a];if(!c.disabled)return void T(c.key)}}(0,f.useEffect)((function(){var t=document.getElementById(N);t&&t.scrollIntoView&&t.scrollIntoView(!1)}),[R]),(0,f.useEffect)((function(){S||T(null)}),[S]);var O=(0,a.Z)({},g?"marginRight":"marginLeft",h);r.length||(O.visibility="hidden",O.order=1);var D=d()((0,a.Z)({},"".concat(L,"-rtl"),g)),j=l?null:f.createElement(X.Z,{prefixCls:L,overlay:B,trigger:["hover"],visible:!!r.length&&S,transitionName:p,onVisibleChange:C,overlayClassName:d()(D,y),mouseEnterDelay:.1,mouseLeaveDelay:.1,getPopupContainer:x},f.createElement("button",{type:"button",className:"".concat(n,"-nav-more"),style:O,tabIndex:-1,"aria-hidden":"true","aria-haspopup":"listbox","aria-controls":I,id:"".concat(c,"-more"),"aria-expanded":S,onKeyDown:function(t){var e=t.which;if(S)switch(e){case F.Z.UP:z(-1),t.preventDefault();break;case F.Z.DOWN:z(1),t.preventDefault();break;case F.Z.ESC:C(!1);break;case F.Z.SPACE:case F.Z.ENTER:null!==R&&k(R,t)}else[F.Z.DOWN,F.Z.SPACE,F.Z.ENTER].includes(e)&&(C(!0),t.preventDefault())}},u));return f.createElement("div",{className:d()("".concat(n,"-nav-operations"),b),style:v,ref:e},j,f.createElement(H,{prefixCls:n,locale:i,editable:m}))}var V=f.memo(f.forwardRef(q),(function(t,e){return e.tabMoving}));var Y=function(t){var e,n=t.prefixCls,o=t.id,c=t.active,r=t.tab,i=r.key,l=r.label,s=r.disabled,u=r.closeIcon,p=t.closable,v=t.renderWrapper,b=t.removeAriaLabel,m=t.editable,h=t.onClick,g=t.onFocus,Z=t.style,k="".concat(n,"-tab"),x=G(p,u,m,s);function y(t){s||h(t)}var _=f.createElement("div",{key:i,"data-node-key":j(i),className:d()(k,(e={},(0,a.Z)(e,"".concat(k,"-with-remove"),x),(0,a.Z)(e,"".concat(k,"-active"),c),(0,a.Z)(e,"".concat(k,"-disabled"),s),e)),style:Z,onClick:y},f.createElement("div",{role:"tab","aria-selected":c,id:o&&"".concat(o,"-tab-").concat(i),className:"".concat(k,"-btn"),"aria-controls":o&&"".concat(o,"-panel-").concat(i),"aria-disabled":s,tabIndex:s?null:0,onClick:function(t){t.stopPropagation(),y(t)},onKeyDown:function(t){[F.Z.SPACE,F.Z.ENTER].includes(t.which)&&(t.preventDefault(),y(t))},onFocus:g},l),x&&f.createElement("button",{type:"button","aria-label":b||"remove",tabIndex:0,className:"".concat(k,"-remove"),onClick:function(t){var e;t.stopPropagation(),(e=t).preventDefault(),e.stopPropagation(),m.onEdit("remove",{key:i,event:e})}},u||m.removeIcon||"\xd7"));return v?v(_):_},Q=function(t){var e=t.current||{},n=e.offsetWidth,a=void 0===n?0:n,o=e.offsetHeight;return[a,void 0===o?0:o]},J=function(t,e){return t[e?0:1]};function U(t,e){var n,c=f.useContext(g),r=c.prefixCls,i=c.tabs,l=t.className,p=t.style,v=t.id,b=t.animated,m=t.activeKey,h=t.rtl,Z=t.extra,k=t.editable,x=t.locale,y=t.tabPosition,M=t.tabBarGutter,D=t.children,G=t.onTabClick,A=t.onTabScroll,X=(0,f.useRef)(),K=(0,f.useRef)(),F=(0,f.useRef)(),q=(0,f.useRef)(),U=(0,f.useRef)(),$=(0,f.useRef)(),tt=(0,f.useRef)(),et="top"===y||"bottom"===y,nt=R(0,(function(t,e){et&&A&&A({direction:t>e?"left":"right"})})),at=(0,o.Z)(nt,2),ot=at[0],ct=at[1],rt=R(0,(function(t,e){!et&&A&&A({direction:t>e?"top":"bottom"})})),it=(0,o.Z)(rt,2),lt=it[0],dt=it[1],st=(0,f.useState)([0,0]),ut=(0,o.Z)(st,2),pt=ut[0],vt=ut[1],ft=(0,f.useState)([0,0]),bt=(0,o.Z)(ft,2),mt=bt[0],ht=bt[1],gt=(0,f.useState)([0,0]),Zt=(0,o.Z)(gt,2),kt=Zt[0],xt=Zt[1],yt=(0,f.useState)([0,0]),_t=(0,o.Z)(yt,2),wt=_t[0],St=_t[1],Ct=function(t){var e=(0,f.useRef)([]),n=(0,f.useState)({}),a=(0,o.Z)(n,2)[1],c=(0,f.useRef)("function"===typeof t?t():t),r=B((function(){var t=c.current;e.current.forEach((function(e){t=e(t)})),e.current=[],c.current=t,a({})}));return[c.current,function(t){e.current.push(t),r()}]}(new Map),Et=(0,o.Z)(Ct,2),Pt=Et[0],Rt=Et[1],Tt=function(t,e,n){return(0,f.useMemo)((function(){for(var n,a=new Map,o=e.get(null===(n=t[0])||void 0===n?void 0:n.key)||P,c=o.left+o.width,r=0;r<t.length;r+=1){var i,l=t[r].key,d=e.get(l);d||(d=e.get(null===(i=t[r-1])||void 0===i?void 0:i.key)||P);var s=a.get(l)||(0,u.Z)({},d);s.right=c-s.left-s.width,a.set(l,s)}return a}),[t.map((function(t){return t.key})).join("_"),e,n])}(i,Pt,mt[0]),It=J(pt,et),Lt=J(mt,et),Nt=J(kt,et),Mt=J(wt,et),Bt=It<Lt+Nt,zt=Bt?It-Mt:It-Nt,Ot="".concat(r,"-nav-operations-hidden"),Dt=0,jt=0;function Gt(t){return t<Dt?Dt:t>jt?jt:t}et&&h?(Dt=0,jt=Math.max(0,Lt-zt)):(Dt=Math.min(0,zt-Lt),jt=0);var At=(0,f.useRef)(),Ht=(0,f.useState)(),Wt=(0,o.Z)(Ht,2),Xt=Wt[0],Kt=Wt[1];function Ft(){Kt(Date.now())}function qt(){window.clearTimeout(At.current)}!function(t,e){var n=(0,f.useState)(),a=(0,o.Z)(n,2),c=a[0],r=a[1],i=(0,f.useState)(0),l=(0,o.Z)(i,2),d=l[0],s=l[1],u=(0,f.useState)(0),p=(0,o.Z)(u,2),v=p[0],b=p[1],m=(0,f.useState)(),h=(0,o.Z)(m,2),g=h[0],Z=h[1],k=(0,f.useRef)(),x=(0,f.useRef)(),y=(0,f.useRef)(null);y.current={onTouchStart:function(t){var e=t.touches[0],n=e.screenX,a=e.screenY;r({x:n,y:a}),window.clearInterval(k.current)},onTouchMove:function(t){if(c){t.preventDefault();var n=t.touches[0],a=n.screenX,o=n.screenY;r({x:a,y:o});var i=a-c.x,l=o-c.y;e(i,l);var u=Date.now();s(u),b(u-d),Z({x:i,y:l})}},onTouchEnd:function(){if(c&&(r(null),Z(null),g)){var t=g.x/v,n=g.y/v,a=Math.abs(t),o=Math.abs(n);if(Math.max(a,o)<T)return;var i=t,l=n;k.current=window.setInterval((function(){Math.abs(i)<I&&Math.abs(l)<I?window.clearInterval(k.current):e((i*=N)*L,(l*=N)*L)}),L)}},onWheel:function(t){var n=t.deltaX,a=t.deltaY,o=0,c=Math.abs(n),r=Math.abs(a);c===r?o="x"===x.current?n:a:c>r?(o=n,x.current="x"):(o=a,x.current="y"),e(-o,-o)&&t.preventDefault()}},f.useEffect((function(){function e(t){y.current.onTouchMove(t)}function n(t){y.current.onTouchEnd(t)}return document.addEventListener("touchmove",e,{passive:!1}),document.addEventListener("touchend",n,{passive:!1}),t.current.addEventListener("touchstart",(function(t){y.current.onTouchStart(t)}),{passive:!1}),t.current.addEventListener("wheel",(function(t){y.current.onWheel(t)})),function(){document.removeEventListener("touchmove",e),document.removeEventListener("touchend",n)}}),[])}(q,(function(t,e){function n(t,e){t((function(t){return Gt(t+e)}))}return!!Bt&&(et?n(ct,t):n(dt,e),qt(),Ft(),!0)})),(0,f.useEffect)((function(){return qt(),Xt&&(At.current=window.setTimeout((function(){Kt(0)}),100)),qt}),[Xt]);var Vt=function(t,e,n,a,o,c,r){var i,l,d,s=r.tabs,u=r.tabPosition,p=r.rtl;return["top","bottom"].includes(u)?(i="width",l=p?"right":"left",d=Math.abs(n)):(i="height",l="top",d=-n),(0,f.useMemo)((function(){if(!s.length)return[0,0];for(var n=s.length,a=n,o=0;o<n;o+=1){var c=t.get(s[o].key)||z;if(c[l]+c[i]>d+e){a=o-1;break}}for(var r=0,u=n-1;u>=0;u-=1)if((t.get(s[u].key)||z)[l]<d){r=u+1;break}return r>=a?[0,0]:[r,a]}),[t,e,a,o,c,d,u,s.map((function(t){return t.key})).join("_"),p])}(Tt,zt,et?ot:lt,Lt,Nt,Mt,(0,u.Z)((0,u.Z)({},t),{},{tabs:i})),Yt=(0,o.Z)(Vt,2),Qt=Yt[0],Jt=Yt[1],Ut=(0,S.Z)((function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:m,e=Tt.get(t)||{width:0,height:0,left:0,right:0,top:0};if(et){var n=ot;h?e.right<ot?n=e.right:e.right+e.width>ot+zt&&(n=e.right+e.width-zt):e.left<-ot?n=-e.left:e.left+e.width>-ot+zt&&(n=-(e.left+e.width-zt)),dt(0),ct(Gt(n))}else{var a=lt;e.top<-lt?a=-e.top:e.top+e.height>-lt+zt&&(a=-(e.top+e.height-zt)),ct(0),dt(Gt(a))}})),$t={};"top"===y||"bottom"===y?$t[h?"marginRight":"marginLeft"]=M:$t.marginTop=M;var te=i.map((function(t,e){var n=t.key;return f.createElement(Y,{id:v,prefixCls:r,key:n,tab:t,style:0===e?void 0:$t,closable:t.closable,editable:k,active:n===m,renderWrapper:D,removeAriaLabel:null===x||void 0===x?void 0:x.removeAriaLabel,onClick:function(t){G(n,t)},onFocus:function(){Ut(n),Ft(),q.current&&(h||(q.current.scrollLeft=0),q.current.scrollTop=0)}})})),ee=function(){return Rt((function(){var t=new Map;return i.forEach((function(e){var n,a=e.key,o=null===(n=U.current)||void 0===n?void 0:n.querySelector('[data-node-key="'.concat(j(a),'"]'));o&&t.set(a,{width:o.offsetWidth,height:o.offsetHeight,left:o.offsetLeft,top:o.offsetTop})})),t}))};(0,f.useEffect)((function(){ee()}),[i.map((function(t){return t.key})).join("_")]);var ne=B((function(){var t=Q(X),e=Q(K),n=Q(F);vt([t[0]-e[0]-n[0],t[1]-e[1]-n[1]]);var a=Q(tt);xt(a);var o=Q($);St(o);var c=Q(U);ht([c[0]-a[0],c[1]-a[1]]),ee()})),ae=i.slice(0,Qt),oe=i.slice(Jt+1),ce=[].concat((0,_.Z)(ae),(0,_.Z)(oe)),re=(0,f.useState)(),ie=(0,o.Z)(re,2),le=ie[0],de=ie[1],se=Tt.get(m),ue=(0,f.useRef)();function pe(){C.Z.cancel(ue.current)}(0,f.useEffect)((function(){var t={};return se&&(et?(h?t.right=se.right:t.left=se.left,t.width=se.width):(t.top=se.top,t.height=se.height)),pe(),ue.current=(0,C.Z)((function(){de(t)})),pe}),[se,et,h]),(0,f.useEffect)((function(){Ut()}),[m,Dt,jt,O(se),O(Tt),et]),(0,f.useEffect)((function(){ne()}),[h]);var ve,fe,be,me,he=!!ce.length,ge="".concat(r,"-nav-wrap");return et?h?(fe=ot>0,ve=ot!==jt):(ve=ot<0,fe=ot!==Dt):(be=lt<0,me=lt!==Dt),f.createElement(w.Z,{onResize:ne},f.createElement("div",{ref:(0,E.x1)(e,X),role:"tablist",className:d()("".concat(r,"-nav"),l),style:p,onKeyDown:function(){Ft()}},f.createElement(W,{ref:K,position:"left",extra:Z,prefixCls:r}),f.createElement("div",{className:d()(ge,(n={},(0,a.Z)(n,"".concat(ge,"-ping-left"),ve),(0,a.Z)(n,"".concat(ge,"-ping-right"),fe),(0,a.Z)(n,"".concat(ge,"-ping-top"),be),(0,a.Z)(n,"".concat(ge,"-ping-bottom"),me),n)),ref:q},f.createElement(w.Z,{onResize:ne},f.createElement("div",{ref:U,className:"".concat(r,"-nav-list"),style:{transform:"translate(".concat(ot,"px, ").concat(lt,"px)"),transition:Xt?"none":void 0}},te,f.createElement(H,{ref:tt,prefixCls:r,locale:x,editable:k,style:(0,u.Z)((0,u.Z)({},0===te.length?void 0:$t),{},{visibility:he?"hidden":null})}),f.createElement("div",{className:d()("".concat(r,"-ink-bar"),(0,a.Z)({},"".concat(r,"-ink-bar-animated"),b.inkBar)),style:le})))),f.createElement(V,(0,s.Z)({},t,{removeAriaLabel:null===x||void 0===x?void 0:x.removeAriaLabel,ref:$,prefixCls:r,tabs:ce,className:!he&&Ot,tabMoving:!!Xt})),f.createElement(W,{ref:F,position:"right",extra:Z,prefixCls:r})))}var $=f.forwardRef(U),tt=["renderTabBar"],et=["label","key"];function nt(t){var e=t.renderTabBar,n=(0,v.Z)(t,tt),a=f.useContext(g).tabs;return e?e((0,u.Z)((0,u.Z)({},n),{},{panes:a.map((function(t){var e=t.label,n=t.key,a=(0,v.Z)(t,et);return f.createElement(k,(0,s.Z)({tab:e,key:n,tabKey:n},a))}))}),$):f.createElement($,n)}n(7738);var at=["id","prefixCls","className","items","direction","activeKey","defaultActiveKey","editable","animated","tabPosition","tabBarGutter","tabBarStyle","tabBarExtraContent","locale","moreIcon","moreTransitionName","destroyInactiveTabPane","renderTabBar","onChange","onTabClick","onTabScroll","getPopupContainer","popupClassName"],ot=0;function ct(t,e){var n,c=t.id,r=t.prefixCls,i=void 0===r?"rc-tabs":r,l=t.className,h=t.items,Z=t.direction,k=t.activeKey,x=t.defaultActiveKey,_=t.editable,w=t.animated,S=t.tabPosition,C=void 0===S?"top":S,E=t.tabBarGutter,P=t.tabBarStyle,R=t.tabBarExtraContent,T=t.locale,I=t.moreIcon,L=t.moreTransitionName,N=t.destroyInactiveTabPane,M=t.renderTabBar,B=t.onChange,z=t.onTabClick,O=t.onTabScroll,D=t.getPopupContainer,j=t.popupClassName,G=(0,v.Z)(t,at),A=f.useMemo((function(){return(h||[]).filter((function(t){return t&&"object"===(0,p.Z)(t)&&"key"in t}))}),[h]),H="rtl"===Z,W=function(){var t,e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{inkBar:!0,tabPane:!1};return(t=!1===e?{inkBar:!1,tabPane:!1}:!0===e?{inkBar:!0,tabPane:!1}:(0,u.Z)({inkBar:!0},"object"===(0,p.Z)(e)?e:{})).tabPaneMotion&&void 0===t.tabPane&&(t.tabPane=!0),!t.tabPaneMotion&&t.tabPane&&(t.tabPane=!1),t}(w),X=(0,f.useState)(!1),K=(0,o.Z)(X,2),F=K[0],q=K[1];(0,f.useEffect)((function(){q((0,b.Z)())}),[]);var V=(0,m.Z)((function(){var t;return null===(t=A[0])||void 0===t?void 0:t.key}),{value:k,defaultValue:x}),Y=(0,o.Z)(V,2),Q=Y[0],J=Y[1],U=(0,f.useState)((function(){return A.findIndex((function(t){return t.key===Q}))})),$=(0,o.Z)(U,2),tt=$[0],et=$[1];(0,f.useEffect)((function(){var t,e=A.findIndex((function(t){return t.key===Q}));-1===e&&(e=Math.max(0,Math.min(tt,A.length-1)),J(null===(t=A[e])||void 0===t?void 0:t.key));et(e)}),[A.map((function(t){return t.key})).join("_"),Q,tt]);var ct=(0,m.Z)(null,{value:c}),rt=(0,o.Z)(ct,2),it=rt[0],lt=rt[1];(0,f.useEffect)((function(){c||(lt("rc-tabs-".concat(ot)),ot+=1)}),[]);var dt={id:it,activeKey:Q,animated:W,tabPosition:C,rtl:H,mobile:F},st=(0,u.Z)((0,u.Z)({},dt),{},{editable:_,locale:T,moreIcon:I,moreTransitionName:L,tabBarGutter:E,onTabClick:function(t,e){null===z||void 0===z||z(t,e);var n=t!==Q;J(t),n&&(null===B||void 0===B||B(t))},onTabScroll:O,extra:R,style:P,panes:null,getPopupContainer:D,popupClassName:j});return f.createElement(g.Provider,{value:{tabs:A,prefixCls:i}},f.createElement("div",(0,s.Z)({ref:e,id:c,className:d()(i,"".concat(i,"-").concat(C),(n={},(0,a.Z)(n,"".concat(i,"-mobile"),F),(0,a.Z)(n,"".concat(i,"-editable"),_),(0,a.Z)(n,"".concat(i,"-rtl"),H),n),l)},G),undefined,f.createElement(nt,(0,s.Z)({},st,{renderTabBar:M})),f.createElement(y,(0,s.Z)({destroyInactiveTabPane:N},dt,{animated:W}))))}var rt=f.forwardRef(ct),it=n(564),lt=n(6569);var dt=function(){return null},st=n(7189),ut={motionAppear:!1,motionEnter:!0,motionLeave:!0};var pt=n(5882),vt=function(t,e){var n={};for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&e.indexOf(a)<0&&(n[a]=t[a]);if(null!=t&&"function"===typeof Object.getOwnPropertySymbols){var o=0;for(a=Object.getOwnPropertySymbols(t);o<a.length;o++)e.indexOf(a[o])<0&&Object.prototype.propertyIsEnumerable.call(t,a[o])&&(n[a[o]]=t[a[o]])}return n};var ft=n(1480),bt=n(111),mt=n(1157),ht=n(9743),gt=function(t){var e=t.componentCls,n=t.motionDurationSlow;return[(0,a.Z)({},e,(0,a.Z)({},"".concat(e,"-switch"),{"&-appear, &-enter":{transition:"none","&-start":{opacity:0},"&-active":{opacity:1,transition:"opacity ".concat(n)}},"&-leave":{position:"absolute",transition:"none",inset:0,"&-start":{opacity:1},"&-active":{opacity:0,transition:"opacity ".concat(n)}}})),[(0,ht.oN)(t,"slide-up"),(0,ht.oN)(t,"slide-down")]]},Zt=function(t){var e,n,o,c,r,i,l=t.componentCls,d=t.tabsCardPadding,s=t.cardBg,u=t.cardGutter,p=t.colorBorderSecondary,v=t.itemSelectedColor;return(0,a.Z)({},"".concat(l,"-card"),(i={},(0,a.Z)(i,"> ".concat(l,"-nav, > div > ").concat(l,"-nav"),(e={},(0,a.Z)(e,"".concat(l,"-tab"),{margin:0,padding:d,background:s,border:"".concat(t.lineWidth,"px ").concat(t.lineType," ").concat(p),transition:"all ".concat(t.motionDurationSlow," ").concat(t.motionEaseInOut)}),(0,a.Z)(e,"".concat(l,"-tab-active"),{color:v,background:t.colorBgContainer}),(0,a.Z)(e,"".concat(l,"-ink-bar"),{visibility:"hidden"}),e)),(0,a.Z)(i,"&".concat(l,"-top, &").concat(l,"-bottom"),(0,a.Z)({},"> ".concat(l,"-nav, > div > ").concat(l,"-nav"),(0,a.Z)({},"".concat(l,"-tab + ").concat(l,"-tab"),{marginLeft:{_skip_check_:!0,value:"".concat(u,"px")}}))),(0,a.Z)(i,"&".concat(l,"-top"),(0,a.Z)({},"> ".concat(l,"-nav, > div > ").concat(l,"-nav"),(n={},(0,a.Z)(n,"".concat(l,"-tab"),{borderRadius:"".concat(t.borderRadiusLG,"px ").concat(t.borderRadiusLG,"px 0 0")}),(0,a.Z)(n,"".concat(l,"-tab-active"),{borderBottomColor:t.colorBgContainer}),n))),(0,a.Z)(i,"&".concat(l,"-bottom"),(0,a.Z)({},"> ".concat(l,"-nav, > div > ").concat(l,"-nav"),(o={},(0,a.Z)(o,"".concat(l,"-tab"),{borderRadius:"0 0 ".concat(t.borderRadiusLG,"px ").concat(t.borderRadiusLG,"px")}),(0,a.Z)(o,"".concat(l,"-tab-active"),{borderTopColor:t.colorBgContainer}),o))),(0,a.Z)(i,"&".concat(l,"-left, &").concat(l,"-right"),(0,a.Z)({},"> ".concat(l,"-nav, > div > ").concat(l,"-nav"),(0,a.Z)({},"".concat(l,"-tab + ").concat(l,"-tab"),{marginTop:"".concat(u,"px")}))),(0,a.Z)(i,"&".concat(l,"-left"),(0,a.Z)({},"> ".concat(l,"-nav, > div > ").concat(l,"-nav"),(c={},(0,a.Z)(c,"".concat(l,"-tab"),{borderRadius:{_skip_check_:!0,value:"".concat(t.borderRadiusLG,"px 0 0 ").concat(t.borderRadiusLG,"px")}}),(0,a.Z)(c,"".concat(l,"-tab-active"),{borderRightColor:{_skip_check_:!0,value:t.colorBgContainer}}),c))),(0,a.Z)(i,"&".concat(l,"-right"),(0,a.Z)({},"> ".concat(l,"-nav, > div > ").concat(l,"-nav"),(r={},(0,a.Z)(r,"".concat(l,"-tab"),{borderRadius:{_skip_check_:!0,value:"0 ".concat(t.borderRadiusLG,"px ").concat(t.borderRadiusLG,"px 0")}}),(0,a.Z)(r,"".concat(l,"-tab-active"),{borderLeftColor:{_skip_check_:!0,value:t.colorBgContainer}}),r))),i))},kt=function(t){var e=t.componentCls,n=t.itemHoverColor,o=t.dropdownEdgeChildVerticalPadding;return(0,a.Z)({},"".concat(e,"-dropdown"),Object.assign(Object.assign({},(0,ft.Wf)(t)),(0,a.Z)({position:"absolute",top:-9999,left:{_skip_check_:!0,value:-9999},zIndex:t.zIndexPopup,display:"block","&-hidden":{display:"none"}},"".concat(e,"-dropdown-menu"),{maxHeight:t.tabsDropdownHeight,margin:0,padding:"".concat(o,"px 0"),overflowX:"hidden",overflowY:"auto",textAlign:{_skip_check_:!0,value:"left"},listStyleType:"none",backgroundColor:t.colorBgContainer,backgroundClip:"padding-box",borderRadius:t.borderRadiusLG,outline:"none",boxShadow:t.boxShadowSecondary,"&-item":Object.assign(Object.assign({},ft.vS),{display:"flex",alignItems:"center",minWidth:t.tabsDropdownWidth,margin:0,padding:"".concat(t.paddingXXS,"px ").concat(t.paddingSM,"px"),color:t.colorText,fontWeight:"normal",fontSize:t.fontSize,lineHeight:t.lineHeight,cursor:"pointer",transition:"all ".concat(t.motionDurationSlow),"> span":{flex:1,whiteSpace:"nowrap"},"&-remove":{flex:"none",marginLeft:{_skip_check_:!0,value:t.marginSM},color:t.colorTextDescription,fontSize:t.fontSizeSM,background:"transparent",border:0,cursor:"pointer","&:hover":{color:n}},"&:hover":{background:t.controlItemBgHover},"&-disabled":{"&, &:hover":{color:t.colorTextDisabled,background:"transparent",cursor:"not-allowed"}}})})))},xt=function(t){var e,n,o,c,r,i,l,d,s=t.componentCls,u=t.margin,p=t.colorBorderSecondary,v=t.horizontalMargin,f=t.verticalItemPadding,b=t.verticalItemMargin;return d={},(0,a.Z)(d,"".concat(s,"-top, ").concat(s,"-bottom"),(0,a.Z)({flexDirection:"column"},"> ".concat(s,"-nav, > div > ").concat(s,"-nav"),(n={margin:v,"&::before":{position:"absolute",right:{_skip_check_:!0,value:0},left:{_skip_check_:!0,value:0},borderBottom:"".concat(t.lineWidth,"px ").concat(t.lineType," ").concat(p),content:"''"}},(0,a.Z)(n,"".concat(s,"-ink-bar"),{height:t.lineWidthBold,"&-animated":{transition:"width ".concat(t.motionDurationSlow,", left ").concat(t.motionDurationSlow,",\n            right ").concat(t.motionDurationSlow)}}),(0,a.Z)(n,"".concat(s,"-nav-wrap"),(e={"&::before, &::after":{top:0,bottom:0,width:t.controlHeight},"&::before":{left:{_skip_check_:!0,value:0},boxShadow:t.boxShadowTabsOverflowLeft},"&::after":{right:{_skip_check_:!0,value:0},boxShadow:t.boxShadowTabsOverflowRight}},(0,a.Z)(e,"&".concat(s,"-nav-wrap-ping-left::before"),{opacity:1}),(0,a.Z)(e,"&".concat(s,"-nav-wrap-ping-right::after"),{opacity:1}),e)),n))),(0,a.Z)(d,"".concat(s,"-top"),(0,a.Z)({},"> ".concat(s,"-nav,\n        > div > ").concat(s,"-nav"),(0,a.Z)({"&::before":{bottom:0}},"".concat(s,"-ink-bar"),{bottom:0}))),(0,a.Z)(d,"".concat(s,"-bottom"),(o={},(0,a.Z)(o,"> ".concat(s,"-nav, > div > ").concat(s,"-nav"),(0,a.Z)({order:1,marginTop:"".concat(u,"px"),marginBottom:0,"&::before":{top:0}},"".concat(s,"-ink-bar"),{top:0})),(0,a.Z)(o,"> ".concat(s,"-content-holder, > div > ").concat(s,"-content-holder"),{order:0}),o)),(0,a.Z)(d,"".concat(s,"-left, ").concat(s,"-right"),(0,a.Z)({},"> ".concat(s,"-nav, > div > ").concat(s,"-nav"),(r={flexDirection:"column",minWidth:1.25*t.controlHeight},(0,a.Z)(r,"".concat(s,"-tab"),{padding:f,textAlign:"center"}),(0,a.Z)(r,"".concat(s,"-tab + ").concat(s,"-tab"),{margin:b}),(0,a.Z)(r,"".concat(s,"-nav-wrap"),(c={flexDirection:"column","&::before, &::after":{right:{_skip_check_:!0,value:0},left:{_skip_check_:!0,value:0},height:t.controlHeight},"&::before":{top:0,boxShadow:t.boxShadowTabsOverflowTop},"&::after":{bottom:0,boxShadow:t.boxShadowTabsOverflowBottom}},(0,a.Z)(c,"&".concat(s,"-nav-wrap-ping-top::before"),{opacity:1}),(0,a.Z)(c,"&".concat(s,"-nav-wrap-ping-bottom::after"),{opacity:1}),c)),(0,a.Z)(r,"".concat(s,"-ink-bar"),{width:t.lineWidthBold,"&-animated":{transition:"height ".concat(t.motionDurationSlow,", top ").concat(t.motionDurationSlow)}}),(0,a.Z)(r,"".concat(s,"-nav-list, ").concat(s,"-nav-operations"),{flex:"1 0 auto",flexDirection:"column"}),r))),(0,a.Z)(d,"".concat(s,"-left"),(i={},(0,a.Z)(i,"> ".concat(s,"-nav, > div > ").concat(s,"-nav"),(0,a.Z)({},"".concat(s,"-ink-bar"),{right:{_skip_check_:!0,value:0}})),(0,a.Z)(i,"> ".concat(s,"-content-holder, > div > ").concat(s,"-content-holder"),(0,a.Z)({marginLeft:{_skip_check_:!0,value:"-".concat(t.lineWidth,"px")},borderLeft:{_skip_check_:!0,value:"".concat(t.lineWidth,"px ").concat(t.lineType," ").concat(t.colorBorder)}},"> ".concat(s,"-content > ").concat(s,"-tabpane"),{paddingLeft:{_skip_check_:!0,value:t.paddingLG}})),i)),(0,a.Z)(d,"".concat(s,"-right"),(l={},(0,a.Z)(l,"> ".concat(s,"-nav, > div > ").concat(s,"-nav"),(0,a.Z)({order:1},"".concat(s,"-ink-bar"),{left:{_skip_check_:!0,value:0}})),(0,a.Z)(l,"> ".concat(s,"-content-holder, > div > ").concat(s,"-content-holder"),(0,a.Z)({order:0,marginRight:{_skip_check_:!0,value:-t.lineWidth},borderRight:{_skip_check_:!0,value:"".concat(t.lineWidth,"px ").concat(t.lineType," ").concat(t.colorBorder)}},"> ".concat(s,"-content > ").concat(s,"-tabpane"),{paddingRight:{_skip_check_:!0,value:t.paddingLG}})),l)),d},yt=function(t){var e,n,o,c=t.componentCls,r=t.cardPaddingSM,i=t.cardPaddingLG,l=t.horizontalItemPaddingSM,d=t.horizontalItemPaddingLG;return o={},(0,a.Z)(o,c,{"&-small":(0,a.Z)({},"> ".concat(c,"-nav"),(0,a.Z)({},"".concat(c,"-tab"),{padding:l,fontSize:t.titleFontSizeSM})),"&-large":(0,a.Z)({},"> ".concat(c,"-nav"),(0,a.Z)({},"".concat(c,"-tab"),{padding:d,fontSize:t.titleFontSizeLG}))}),(0,a.Z)(o,"".concat(c,"-card"),(n={},(0,a.Z)(n,"&".concat(c,"-small"),(e={},(0,a.Z)(e,"> ".concat(c,"-nav"),(0,a.Z)({},"".concat(c,"-tab"),{padding:r})),(0,a.Z)(e,"&".concat(c,"-bottom"),(0,a.Z)({},"> ".concat(c,"-nav ").concat(c,"-tab"),{borderRadius:"0 0 ".concat(t.borderRadius,"px ").concat(t.borderRadius,"px")})),(0,a.Z)(e,"&".concat(c,"-top"),(0,a.Z)({},"> ".concat(c,"-nav ").concat(c,"-tab"),{borderRadius:"".concat(t.borderRadius,"px ").concat(t.borderRadius,"px 0 0")})),(0,a.Z)(e,"&".concat(c,"-right"),(0,a.Z)({},"> ".concat(c,"-nav ").concat(c,"-tab"),{borderRadius:{_skip_check_:!0,value:"0 ".concat(t.borderRadius,"px ").concat(t.borderRadius,"px 0")}})),(0,a.Z)(e,"&".concat(c,"-left"),(0,a.Z)({},"> ".concat(c,"-nav ").concat(c,"-tab"),{borderRadius:{_skip_check_:!0,value:"".concat(t.borderRadius,"px 0 0 ").concat(t.borderRadius,"px")}})),e)),(0,a.Z)(n,"&".concat(c,"-large"),(0,a.Z)({},"> ".concat(c,"-nav"),(0,a.Z)({},"".concat(c,"-tab"),{padding:i}))),n)),o},_t=function(t){var e,n,o,c,r,i=t.componentCls,l=t.tabsHorizontalItemMarginRTL,d=t.iconCls,s=t.cardGutter,u="".concat(i,"-rtl");return r={},(0,a.Z)(r,u,(c={direction:"rtl"},(0,a.Z)(c,"".concat(i,"-nav"),(0,a.Z)({},"".concat(i,"-tab"),(e={margin:{_skip_check_:!0,value:l}},(0,a.Z)(e,"".concat(i,"-tab:last-of-type"),{marginLeft:{_skip_check_:!0,value:0}}),(0,a.Z)(e,d,{marginRight:{_skip_check_:!0,value:0},marginLeft:{_skip_check_:!0,value:"".concat(t.marginSM,"px")}}),(0,a.Z)(e,"".concat(i,"-tab-remove"),(0,a.Z)({marginRight:{_skip_check_:!0,value:"".concat(t.marginXS,"px")},marginLeft:{_skip_check_:!0,value:"-".concat(t.marginXXS,"px")}},d,{margin:0})),e))),(0,a.Z)(c,"&".concat(i,"-left"),(n={},(0,a.Z)(n,"> ".concat(i,"-nav"),{order:1}),(0,a.Z)(n,"> ".concat(i,"-content-holder"),{order:0}),n)),(0,a.Z)(c,"&".concat(i,"-right"),(o={},(0,a.Z)(o,"> ".concat(i,"-nav"),{order:0}),(0,a.Z)(o,"> ".concat(i,"-content-holder"),{order:1}),o)),(0,a.Z)(c,"&".concat(i,"-card").concat(i,"-top, &").concat(i,"-card").concat(i,"-bottom"),(0,a.Z)({},"> ".concat(i,"-nav, > div > ").concat(i,"-nav"),(0,a.Z)({},"".concat(i,"-tab + ").concat(i,"-tab"),{marginRight:{_skip_check_:!0,value:s},marginLeft:{_skip_check_:!0,value:0}}))),c)),(0,a.Z)(r,"".concat(i,"-dropdown-rtl"),{direction:"rtl"}),(0,a.Z)(r,"".concat(i,"-menu-item"),(0,a.Z)({},"".concat(i,"-dropdown-rtl"),{textAlign:{_skip_check_:!0,value:"right"}})),r},wt=function(t){var e,n,o,c,r=t.componentCls,i=t.tabsCardPadding,l=t.cardHeight,d=t.cardGutter,s=t.itemHoverColor,u=t.itemActiveColor,p=t.colorBorderSecondary;return c={},(0,a.Z)(c,r,Object.assign(Object.assign(Object.assign(Object.assign({},(0,ft.Wf)(t)),(n={display:"flex"},(0,a.Z)(n,"> ".concat(r,"-nav, > div > ").concat(r,"-nav"),(e={position:"relative",display:"flex",flex:"none",alignItems:"center"},(0,a.Z)(e,"".concat(r,"-nav-wrap"),{position:"relative",display:"flex",flex:"auto",alignSelf:"stretch",overflow:"hidden",whiteSpace:"nowrap",transform:"translate(0)","&::before, &::after":{position:"absolute",zIndex:1,opacity:0,transition:"opacity ".concat(t.motionDurationSlow),content:"''",pointerEvents:"none"}}),(0,a.Z)(e,"".concat(r,"-nav-list"),{position:"relative",display:"flex",transition:"opacity ".concat(t.motionDurationSlow)}),(0,a.Z)(e,"".concat(r,"-nav-operations"),{display:"flex",alignSelf:"stretch"}),(0,a.Z)(e,"".concat(r,"-nav-operations-hidden"),{position:"absolute",visibility:"hidden",pointerEvents:"none"}),(0,a.Z)(e,"".concat(r,"-nav-more"),{position:"relative",padding:i,background:"transparent",border:0,color:t.colorText,"&::after":{position:"absolute",right:{_skip_check_:!0,value:0},bottom:0,left:{_skip_check_:!0,value:0},height:t.controlHeightLG/8,transform:"translateY(100%)",content:"''"}}),(0,a.Z)(e,"".concat(r,"-nav-add"),Object.assign({minWidth:l,marginLeft:{_skip_check_:!0,value:d},padding:"0 ".concat(t.paddingXS,"px"),background:"transparent",border:"".concat(t.lineWidth,"px ").concat(t.lineType," ").concat(p),borderRadius:"".concat(t.borderRadiusLG,"px ").concat(t.borderRadiusLG,"px 0 0"),outline:"none",cursor:"pointer",color:t.colorText,transition:"all ".concat(t.motionDurationSlow," ").concat(t.motionEaseInOut),"&:hover":{color:s},"&:active, &:focus:not(:focus-visible)":{color:u}},(0,ft.Qy)(t))),e)),(0,a.Z)(n,"".concat(r,"-extra-content"),{flex:"none"}),(0,a.Z)(n,"".concat(r,"-ink-bar"),{position:"absolute",background:t.inkBarColor,pointerEvents:"none"}),n)),function(t){var e,n,o=t.componentCls,c=t.itemActiveColor,r=t.itemHoverColor,i=t.iconCls,l=t.tabsHorizontalItemMargin,d=t.horizontalItemPadding,s=t.itemSelectedColor,u="".concat(o,"-tab");return n={},(0,a.Z)(n,u,(e={position:"relative",display:"inline-flex",alignItems:"center",padding:d,fontSize:t.titleFontSize,background:"transparent",border:0,outline:"none",cursor:"pointer","&-btn, &-remove":Object.assign({"&:focus:not(:focus-visible), &:active":{color:c}},(0,ft.Qy)(t)),"&-btn":{outline:"none",transition:"all 0.3s"},"&-remove":{flex:"none",marginRight:{_skip_check_:!0,value:-t.marginXXS},marginLeft:{_skip_check_:!0,value:t.marginXS},color:t.colorTextDescription,fontSize:t.fontSizeSM,background:"transparent",border:"none",outline:"none",cursor:"pointer",transition:"all ".concat(t.motionDurationSlow),"&:hover":{color:t.colorTextHeading}},"&:hover":{color:r}},(0,a.Z)(e,"&".concat(u,"-active ").concat(u,"-btn"),{color:s,textShadow:t.tabsActiveTextShadow}),(0,a.Z)(e,"&".concat(u,"-disabled"),{color:t.colorTextDisabled,cursor:"not-allowed"}),(0,a.Z)(e,"&".concat(u,"-disabled ").concat(u,"-btn, &").concat(u,"-disabled ").concat(o,"-remove"),{"&:focus, &:active":{color:t.colorTextDisabled}}),(0,a.Z)(e,"& ".concat(u,"-remove ").concat(i),{margin:0}),(0,a.Z)(e,i,{marginRight:{_skip_check_:!0,value:t.marginSM}}),e)),(0,a.Z)(n,"".concat(u," + ").concat(u),{margin:{_skip_check_:!0,value:l}}),n}(t)),(o={},(0,a.Z)(o,"".concat(r,"-content"),{position:"relative",width:"100%"}),(0,a.Z)(o,"".concat(r,"-content-holder"),{flex:"auto",minWidth:0,minHeight:0}),(0,a.Z)(o,"".concat(r,"-tabpane"),{outline:"none","&-hidden":{display:"none"}}),o))),(0,a.Z)(c,"".concat(r,"-centered"),(0,a.Z)({},"> ".concat(r,"-nav, > div > ").concat(r,"-nav"),(0,a.Z)({},"".concat(r,"-nav-wrap"),(0,a.Z)({},"&:not([class*='".concat(r,"-nav-wrap-ping'])"),{justifyContent:"center"})))),c},St=(0,bt.Z)("Tabs",(function(t){var e=(0,mt.TS)(t,{tabsCardPadding:t.cardPadding||"".concat((t.cardHeight-Math.round(t.fontSize*t.lineHeight))/2-t.lineWidth,"px ").concat(t.padding,"px"),dropdownEdgeChildVerticalPadding:t.paddingXXS,tabsActiveTextShadow:"0 0 0.25px currentcolor",tabsDropdownHeight:200,tabsDropdownWidth:120,tabsHorizontalItemMargin:"0 0 0 ".concat(t.horizontalItemGutter,"px"),tabsHorizontalItemMarginRTL:"0 0 0 ".concat(t.horizontalItemGutter,"px")});return[yt(e),_t(e),xt(e),kt(e),Zt(e),wt(e),gt(e)]}),(function(t){var e=t.controlHeightLG;return{zIndexPopup:t.zIndexPopupBase+50,cardBg:t.colorFillAlter,cardHeight:e,cardPadding:"",cardPaddingSM:"".concat(1.5*t.paddingXXS,"px ").concat(t.padding,"px"),cardPaddingLG:"".concat(t.paddingXS,"px ").concat(t.padding,"px ").concat(1.5*t.paddingXXS,"px"),titleFontSize:t.fontSize,titleFontSizeLG:t.fontSizeLG,titleFontSizeSM:t.fontSize,inkBarColor:t.colorPrimary,horizontalMargin:"0 0 ".concat(t.margin,"px 0"),horizontalItemGutter:32,horizontalItemMargin:"",horizontalItemMarginRTL:"",horizontalItemPadding:"".concat(t.paddingSM,"px 0"),horizontalItemPaddingSM:"".concat(t.paddingXS,"px 0"),horizontalItemPaddingLG:"".concat(t.padding,"px 0"),verticalItemPadding:"".concat(t.paddingXS,"px ").concat(t.paddingLG,"px"),verticalItemMargin:"".concat(t.margin,"px 0 0 0"),itemSelectedColor:t.colorPrimary,itemHoverColor:t.colorPrimaryHover,itemActiveColor:t.colorPrimaryActive,cardGutter:t.marginXXS/2}})),Ct=function(t,e){var n={};for(var a in t)Object.prototype.hasOwnProperty.call(t,a)&&e.indexOf(a)<0&&(n[a]=t[a]);if(null!=t&&"function"===typeof Object.getOwnPropertySymbols){var o=0;for(a=Object.getOwnPropertySymbols(t);o<a.length;o++)e.indexOf(a[o])<0&&Object.prototype.propertyIsEnumerable.call(t,a[o])&&(n[a[o]]=t[a[o]])}return n},Et=function(t){var e,n,l=t.type,s=t.className,u=t.rootClassName,p=t.size,v=t.onEdit,b=t.hideAdd,m=t.centered,h=t.addIcon,g=t.popupClassName,Z=t.children,k=t.items,x=t.animated,y=t.style,_=Ct(t,["type","className","rootClassName","size","onEdit","hideAdd","centered","addIcon","popupClassName","children","items","animated","style"]),w=_.prefixCls,S=_.moreIcon,C=void 0===S?f.createElement(r.Z,null):S,E=f.useContext(it.E_),P=E.direction,R=E.tabs,T=E.getPrefixCls,I=E.getPopupContainer,L=T("tabs",w),N=St(L),M=(0,o.Z)(N,2),B=M[0],z=M[1];"editable-card"===l&&(n={onEdit:function(t,e){var n=e.key,a=e.event;null===v||void 0===v||v("add"===t?a:n,t)},removeIcon:f.createElement(c.Z,null),addIcon:h||f.createElement(i.Z,null),showAdd:!0!==b});var O=T(),D=function(t,e){return t||function(t){return t.filter((function(t){return t}))}((0,pt.Z)(e).map((function(t){if(f.isValidElement(t)){var e=t.key,n=t.props||{},a=n.tab,o=vt(n,["tab"]);return Object.assign(Object.assign({key:String(e)},o),{label:a})}return null})))}(k,Z),j=function(t){var e,n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{inkBar:!0,tabPane:!1};return(e=!1===n?{inkBar:!1,tabPane:!1}:!0===n?{inkBar:!0,tabPane:!0}:Object.assign({inkBar:!0},"object"===typeof n?n:{})).tabPane&&(e.tabPaneMotion=Object.assign(Object.assign({},ut),{motionName:(0,st.mL)(t,"switch")})),e}(L,x),G=(0,lt.Z)(p),A=Object.assign(Object.assign({},null===R||void 0===R?void 0:R.style),y);return B(f.createElement(rt,Object.assign({direction:P,getPopupContainer:I,moreTransitionName:"".concat(O,"-slide-up")},_,{items:D,className:d()((e={},(0,a.Z)(e,"".concat(L,"-").concat(G),G),(0,a.Z)(e,"".concat(L,"-card"),["card","editable-card"].includes(l)),(0,a.Z)(e,"".concat(L,"-editable-card"),"editable-card"===l),(0,a.Z)(e,"".concat(L,"-centered"),m),e),null===R||void 0===R?void 0:R.className,s,u,z),popupClassName:d()(g,z),style:A,editable:n,moreIcon:C,prefixCls:L,animated:j})))};Et.TabPane=dt;var Pt=Et}}]);
//# sourceMappingURL=600.3407a34e.chunk.js.map