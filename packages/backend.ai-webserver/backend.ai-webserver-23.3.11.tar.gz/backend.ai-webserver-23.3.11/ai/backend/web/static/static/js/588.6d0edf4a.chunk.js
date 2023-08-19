"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[588],{9277:function(e,n,t){var a=t(1413),i=t(4925),r=t(4036),o=(t(4519),t(2556)),l=["direction","wrap","justify","align","gap","style","children"];n.Z=function(e){var n=e.direction,t=void 0===n?"row":n,s=e.wrap,d=void 0===s?"nowrap":s,c=e.justify,u=void 0===c?"flex-start":c,p=e.align,g=void 0===p?"center":p,m=e.gap,f=void 0===m?0:m,y=e.style,h=e.children,v=(0,i.Z)(e,l),_=r.Z.useToken().token,b=[u,g],k=null===b||void 0===b?void 0:b.map((function(e){var n;switch(e){case"start":n="flex-start";break;case"end":n="flex-end";break;case"between":n="space-between";break;case"around":n="space-around";break;default:n=e}return n})),x=(0,a.Z)({display:"flex",flexDirection:t,flexWrap:d,justifyContent:k[0],alignItems:k[1]},y);return(0,o.jsx)("div",(0,a.Z)((0,a.Z)({style:(0,a.Z)({alignItems:"stretch",backgroundColor:"transparent",border:"0 solid black",boxSizing:"border-box",display:"flex",flexBasis:"auto",flexDirection:"column",flexShrink:0,listStyle:"none",margin:0,minHeight:0,minWidth:0,padding:0,position:"relative",textDecoration:"none",gap:"string"===typeof f?_["padding"+f.toUpperCase()]:f},x)},v),{},{children:h}))}},6588:function(e,n,t){t.r(n),t.d(n,{StorageStatusPanelFallback:function(){return R},default:function(){return Y}});var a=t(9439),i=t(4519),r=t(7112),o=t(6980),l=t(1748),s=t(4036),d=t(1534),c=t(867),u=t(5444),p=t(3656),g=t(4942),m=t(3270),f=t.n(m),y=t(564),h=t(1480),v=t(111),_=t(1157),b=function(e){var n,t=e.componentCls,a=e.sizePaddingEdgeHorizontal,i=e.colorSplit,r=e.lineWidth;return(0,g.Z)({},t,Object.assign(Object.assign({},(0,h.Wf)(e)),(n={borderBlockStart:"".concat(r,"px solid ").concat(i),"&-vertical":{position:"relative",top:"-0.06em",display:"inline-block",height:"0.9em",margin:"0 ".concat(e.dividerVerticalGutterMargin,"px"),verticalAlign:"middle",borderTop:0,borderInlineStart:"".concat(r,"px solid ").concat(i)},"&-horizontal":{display:"flex",clear:"both",width:"100%",minWidth:"100%",margin:"".concat(e.dividerHorizontalGutterMargin,"px 0")}},(0,g.Z)(n,"&-horizontal".concat(t,"-with-text"),{display:"flex",alignItems:"center",margin:"".concat(e.dividerHorizontalWithTextGutterMargin,"px 0"),color:e.colorTextHeading,fontWeight:500,fontSize:e.fontSizeLG,whiteSpace:"nowrap",textAlign:"center",borderBlockStart:"0 ".concat(i),"&::before, &::after":{position:"relative",width:"50%",borderBlockStart:"".concat(r,"px solid transparent"),borderBlockStartColor:"inherit",borderBlockEnd:0,transform:"translateY(50%)",content:"''"}}),(0,g.Z)(n,"&-horizontal".concat(t,"-with-text-left"),{"&::before":{width:"5%"},"&::after":{width:"95%"}}),(0,g.Z)(n,"&-horizontal".concat(t,"-with-text-right"),{"&::before":{width:"95%"},"&::after":{width:"5%"}}),(0,g.Z)(n,"".concat(t,"-inner-text"),{display:"inline-block",padding:"0 1em"}),(0,g.Z)(n,"&-dashed",{background:"none",borderColor:i,borderStyle:"dashed",borderWidth:"".concat(r,"px 0 0")}),(0,g.Z)(n,"&-horizontal".concat(t,"-with-text").concat(t,"-dashed"),{"&::before, &::after":{borderStyle:"dashed none none"}}),(0,g.Z)(n,"&-vertical".concat(t,"-dashed"),{borderInlineStartWidth:r,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0}),(0,g.Z)(n,"&-plain".concat(t,"-with-text"),{color:e.colorText,fontWeight:"normal",fontSize:e.fontSize}),(0,g.Z)(n,"&-horizontal".concat(t,"-with-text-left").concat(t,"-no-default-orientation-margin-left"),(0,g.Z)({"&::before":{width:0},"&::after":{width:"100%"}},"".concat(t,"-inner-text"),{paddingInlineStart:a})),(0,g.Z)(n,"&-horizontal".concat(t,"-with-text-right").concat(t,"-no-default-orientation-margin-right"),(0,g.Z)({"&::before":{width:"100%"},"&::after":{width:0}},"".concat(t,"-inner-text"),{paddingInlineEnd:a})),n)))},k=(0,v.Z)("Divider",(function(e){var n=(0,_.TS)(e,{dividerVerticalGutterMargin:e.marginXS,dividerHorizontalWithTextGutterMargin:e.margin,dividerHorizontalGutterMargin:e.marginLG});return[b(n)]}),{sizePaddingEdgeHorizontal:0}),x=function(e,n){var t={};for(var a in e)Object.prototype.hasOwnProperty.call(e,a)&&n.indexOf(a)<0&&(t[a]=e[a]);if(null!=e&&"function"===typeof Object.getOwnPropertySymbols){var i=0;for(a=Object.getOwnPropertySymbols(e);i<a.length;i++)n.indexOf(a[i])<0&&Object.prototype.propertyIsEnumerable.call(e,a[i])&&(t[a[i]]=e[a[i]])}return t};var S=function(e){var n,t=i.useContext(y.E_),r=t.getPrefixCls,o=t.direction,l=e.prefixCls,s=e.type,d=void 0===s?"horizontal":s,c=e.orientation,u=void 0===c?"center":c,p=e.orientationMargin,m=e.className,h=e.rootClassName,v=e.children,_=e.dashed,b=e.plain,S=x(e,["prefixCls","type","orientation","orientationMargin","className","rootClassName","children","dashed","plain"]),w=r("divider",l),j=k(w),Z=(0,a.Z)(j,2),F=Z[0],q=Z[1],z=u.length>0?"-".concat(u):u,T=!!v,Q="left"===u&&null!=p,P="right"===u&&null!=p,K=f()(w,q,"".concat(w,"-").concat(d),(n={},(0,g.Z)(n,"".concat(w,"-with-text"),T),(0,g.Z)(n,"".concat(w,"-with-text").concat(z),T),(0,g.Z)(n,"".concat(w,"-dashed"),!!_),(0,g.Z)(n,"".concat(w,"-plain"),!!b),(0,g.Z)(n,"".concat(w,"-rtl"),"rtl"===o),(0,g.Z)(n,"".concat(w,"-no-default-orientation-margin-left"),Q),(0,g.Z)(n,"".concat(w,"-no-default-orientation-margin-right"),P),n),m,h),L=i.useMemo((function(){return"number"===typeof p?p:/^\d+$/.test(p)?Number(p):p}),[p]),C=Object.assign(Object.assign({},Q&&{marginLeft:L}),P&&{marginRight:L});return F(i.createElement("div",Object.assign({className:K},S,{role:"separator"}),v&&"vertical"!==d&&i.createElement("span",{className:"".concat(w,"-inner-text"),style:C},v)))},w=t(227),j=t(2513),Z=t(4473),F=t(7589),q=t(7462),z={icon:{tag:"svg",attrs:{viewBox:"64 64 896 896",focusable:"false"},children:[{tag:"path",attrs:{d:"M512 64C264.6 64 64 264.6 64 512s200.6 448 448 448 448-200.6 448-448S759.4 64 512 64zm0 820c-205.4 0-372-166.6-372-372s166.6-372 372-372 372 166.6 372 372-166.6 372-372 372z"}},{tag:"path",attrs:{d:"M464 336a48 48 0 1096 0 48 48 0 10-96 0zm72 112h-48c-4.4 0-8 3.6-8 8v272c0 4.4 3.6 8 8 8h48c4.4 0 8-3.6 8-8V456c0-4.4-3.6-8-8-8z"}}]},name:"info-circle",theme:"outlined"},T=t(9491),Q=function(e,n){return i.createElement(T.Z,(0,q.Z)({},e,{ref:n,icon:z}))};var P,K,L,C=i.forwardRef(Q),D=t(9277),I=t(7760),M=t(3255),V=t(2556),B=function(e){var n,a,i,r,d,c=e.usageProgressFrgmt,g=(0,l.$G)().t,m=s.Z.useToken().token,f=(0,o.useFragment)(void 0!==P?P:P=t(407),c),y=parseFloat(null===f||void 0===f||null===(n=f.details)||void 0===n?void 0:n.usage_bytes)||0,h=parseFloat(null===f||void 0===f||null===(a=f.details)||void 0===a?void 0:a.hard_limit_bytes)||0,v=h>0?null===(i=y/h*100)||void 0===i?void 0:i.toFixed(2):0;return(0,V.jsxs)(D.Z,{direction:"column",children:[(0,V.jsx)(u.Z,{size:[180,15],percent:v,strokeColor:(0,M.lA)(v),status:v>=100?"exception":"normal"}),(0,V.jsxs)(D.Z,{direction:"row",gap:m.marginXXS,style:{fontSize:12},children:[(0,V.jsxs)(p.Z.Text,{type:"secondary",style:{fontSize:12},children:[g("data.Used"),":"]}),(0,M.Uz)(null===f||void 0===f||null===(r=f.details)||void 0===r?void 0:r.usage_bytes)," GB",(0,V.jsx)(p.Z.Text,{type:"secondary",style:{fontSize:12},children:" / "}),(0,V.jsxs)(p.Z.Text,{type:"secondary",style:{fontSize:12},children:[g("data.Limit"),":"]}),(0,M.Uz)(null===f||void 0===f||null===(d=f.details)||void 0===d?void 0:d.hard_limit_bytes)," GB"]})]})},$=t(1413),E=t(4925),O=t(1215),N=t(2048),W=t.n(N),A=["value","onChange","autoSelectDefault"],G=function(e){var n=e.value,t=e.onChange,a=e.autoSelectDefault,o=(0,E.Z)(e,A),s=(0,l.$G)().t,d=(0,I.Dj)(),c=(0,r.useQuery)("vhostInfo",(function(){return d.vfolder.list_hosts()}),{suspense:!0}),u=c.data,p=c.isLoading;return(0,i.useEffect)((function(){a&&!n&&null!==u&&void 0!==u&&u.default&&(null===t||void 0===t||t(null===u||void 0===u?void 0:u.default,(0,$.Z)({id:null===u||void 0===u?void 0:u.default},(null===u||void 0===u?void 0:u.volume_info[null===u||void 0===u?void 0:u.default])||{})))}),[]),(0,V.jsx)(O.Z,(0,$.Z)({filterOption:!1,placeholder:s("data.SelectStorageHost"),loading:p,style:{minWidth:165},value:(null===n||void 0===n?void 0:n.id)||n,onChange:function(e){null===t||void 0===t||t(e,(0,$.Z)({id:e},(null===u||void 0===u?void 0:u.volume_info[e])||{}))},options:W().map(null===u||void 0===u?void 0:u.allowed,(function(e){return{value:e,label:e}}))},o))},H=t(2064),U=t(7171),X=function(e){var n=e.style,t=e.children;return(0,V.jsxs)(D.Z,{direction:"row",justify:"center",align:"center",style:(0,$.Z)({width:"100%",height:"100%"},n),children:[(0,V.jsx)(U.Z,{indicator:(0,V.jsx)(H.Z,{spin:!0})}),t]})},R=function(){var e=(0,l.$G)().t;return(0,V.jsx)(d.Z,{size:"small",title:e("data.StorageStatus"),style:{margin:"3px 14px"},children:(0,V.jsx)(F.Z,{active:!0})})},Y=function(e){var n,g,m=e.fetchKey,f=(0,l.$G)().t,y=s.Z.useToken().token,h=(0,I.Dj)(),v=(0,I.qh)(),_=(0,i.useState)(),b=(0,a.Z)(_,2),k=b[0],x=b[1],F=(0,i.useDeferredValue)(k),q=(0,r.useQuery)(["vfolders",{fetchKey:m}],(function(){return h.vfolder.list(null===v||void 0===v?void 0:v.id)}),{suspense:!1}).data,z=null===q||void 0===q?void 0:q.filter((function(e){return e.is_owner&&"user"===e.ownership_type})).length,T=null===q||void 0===q?void 0:q.filter((function(e){return"group"===e.ownership_type})).length,Q=null===q||void 0===q?void 0:q.filter((function(e){return!e.is_owner&&"user"===e.ownership_type})).length,P=(0,o.useLazyLoadQuery)(void 0!==K?K:K=t(4933),{domain_name:(0,I.tQ)(),access_key:null===h||void 0===h?void 0:h._config.accessKey,email:null===h||void 0===h?void 0:h.email}),$=P.keypair,E=P.user,O=(0,o.useLazyLoadQuery)(void 0!==L?L:L=t(5912),{keypair_resource_policy_name:null===$||void 0===$?void 0:$.resource_policy,project_quota_scope_id:(0,M.VQ)("project",null===v||void 0===v?void 0:v.id),user_quota_scope_id:(0,M.VQ)("user",(null===E||void 0===E?void 0:E.id)||""),storage_host_name:(null===F||void 0===F?void 0:F.id)||"",skipQuotaScope:void 0===(null===v||void 0===v?void 0:v.id)||void 0===(null===E||void 0===E?void 0:E.id)||!(null!==F&&void 0!==F&&F.id)}),N=O.keypair_resource_policy,W=O.project_quota_scope,A=O.user_quota_scope,H=(null===N||void 0===N?void 0:N.max_vfolder_count)||0,U=H>0?null===(n=z/H*100)||void 0===n?void 0:n.toFixed(2):0;return(0,V.jsx)(d.Z,{size:"small",title:f("data.StorageStatus"),style:{margin:"3px 14px"},children:(0,V.jsxs)(c.Z,{bordered:!0,column:{xxl:4,xl:4,lg:2,md:1,sm:1,xs:1},size:"small",children:[(0,V.jsxs)(c.Z.Item,{label:f("data.NumberOfFolders"),children:[(0,V.jsx)(u.Z,{size:[200,15],percent:U,strokeColor:(0,M.lA)(U),style:{width:"95%"},status:U>=100?"exception":"normal"}),(0,V.jsxs)(D.Z,{direction:"row",gap:y.marginXXS,wrap:"wrap",children:[(0,V.jsxs)(p.Z.Text,{type:"secondary",children:[f("data.Created"),":"]}),z,(0,V.jsx)(p.Z.Text,{type:"secondary",children:" / "}),(0,V.jsxs)(p.Z.Text,{type:"secondary",children:[f("data.Limit"),":"]}),H]}),(0,V.jsx)(S,{style:{margin:"12px auto"}}),(0,V.jsxs)(D.Z,{direction:"row",wrap:"wrap",justify:"between",children:[(0,V.jsxs)(D.Z,{gap:y.marginXXS,children:[(0,V.jsxs)(p.Z.Text,{type:"secondary",children:[f("data.ProjectFolder"),":"]}),T]}),(0,V.jsxs)(D.Z,{gap:y.marginXXS,style:{marginRight:30},children:[(0,V.jsxs)(p.Z.Text,{type:"secondary",children:[f("data.Invited"),":"]}),Q]})]})]}),(0,V.jsxs)(c.Z.Item,{label:(0,V.jsxs)("div",{children:[f("data.QuotaPerStorageVolume"),(0,V.jsx)(w.Z,{title:f("data.HostDetails"),children:(0,V.jsx)(j.ZP,{type:"link",icon:(0,V.jsx)(C,{})})})]}),children:[(0,V.jsxs)(D.Z,{wrap:"wrap",justify:"between",direction:"row",style:{minWidth:"25vw"},children:[(0,V.jsx)(p.Z.Text,{type:"secondary",children:f("data.Host")}),(0,V.jsx)(G,{onChange:function(e,n){x(n)},value:k,autoSelectDefault:!0})]}),k!==F?(0,V.jsx)(X,{style:{minHeight:120}}):null!==k&&void 0!==k&&null!==(g=k.capabilities)&&void 0!==g&&g.includes("quota")?(0,V.jsxs)(V.Fragment,{children:[(0,V.jsxs)(D.Z,{style:{margin:"15px auto"},justify:"between",wrap:"wrap",children:[(0,V.jsxs)(p.Z.Text,{type:"secondary",style:{wordBreak:"keep-all",wordWrap:"break-word"},children:[f("data.Project"),(0,V.jsx)("br",{}),"(",null===v||void 0===v?void 0:v.name,")"]}),(0,V.jsx)(B,{usageProgressFrgmt:W||null})]}),(0,V.jsxs)(D.Z,{justify:"between",wrap:"wrap",children:[(0,V.jsxs)(p.Z.Text,{type:"secondary",style:{wordBreak:"keep-all",wordWrap:"break-word"},children:[f("data.User"),(0,V.jsx)("br",{}),"(",null===h||void 0===h?void 0:h.email,")"]}),(0,V.jsx)(B,{usageProgressFrgmt:A||null})]})]}):(0,V.jsx)(Z.Z,{image:Z.Z.PRESENTED_IMAGE_SIMPLE,description:f("storageHost.QuotaDoesNotSupported"),style:{margin:"25px auto"}})]})]})})}},4933:function(e,n,t){t.r(n);var a=function(){var e={defaultValue:null,kind:"LocalArgument",name:"access_key"},n={defaultValue:null,kind:"LocalArgument",name:"domain_name"},t={defaultValue:null,kind:"LocalArgument",name:"email"},a={kind:"Variable",name:"domain_name",variableName:"domain_name"},i=[{kind:"Variable",name:"access_key",variableName:"access_key"},a],r={alias:null,args:null,kind:"ScalarField",name:"resource_policy",storageKey:null},o={alias:null,args:null,kind:"ScalarField",name:"id",storageKey:null},l={alias:null,args:[a,{kind:"Variable",name:"email",variableName:"email"}],concreteType:"User",kind:"LinkedField",name:"user",plural:!1,selections:[o],storageKey:null};return{fragment:{argumentDefinitions:[e,n,t],kind:"Fragment",metadata:null,name:"StorageStatusPanelKeypairQuery",selections:[{alias:null,args:i,concreteType:"KeyPair",kind:"LinkedField",name:"keypair",plural:!1,selections:[r],storageKey:null},l],type:"Queries",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[n,e,t],kind:"Operation",name:"StorageStatusPanelKeypairQuery",selections:[{alias:null,args:i,concreteType:"KeyPair",kind:"LinkedField",name:"keypair",plural:!1,selections:[r,o],storageKey:null},l]},params:{cacheID:"c5694f624546bc3205cc2a8efb5f2797",id:null,metadata:{},name:"StorageStatusPanelKeypairQuery",operationKind:"query",text:"query StorageStatusPanelKeypairQuery(\n  $domain_name: String\n  $access_key: String\n  $email: String\n) {\n  keypair(domain_name: $domain_name, access_key: $access_key) {\n    resource_policy\n    id\n  }\n  user(domain_name: $domain_name, email: $email) {\n    id\n  }\n}\n"}}}();a.hash="23480c420d7c3a5eaed1db29b5b0ed31",n.default=a},5912:function(e,n,t){t.r(n);var a=function(){var e={defaultValue:null,kind:"LocalArgument",name:"keypair_resource_policy_name"},n={defaultValue:null,kind:"LocalArgument",name:"project_quota_scope_id"},t={defaultValue:null,kind:"LocalArgument",name:"skipQuotaScope"},a={defaultValue:null,kind:"LocalArgument",name:"storage_host_name"},i={defaultValue:null,kind:"LocalArgument",name:"user_quota_scope_id"},r={alias:null,args:[{kind:"Variable",name:"name",variableName:"keypair_resource_policy_name"}],concreteType:"KeyPairResourcePolicy",kind:"LinkedField",name:"keypair_resource_policy",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"max_vfolder_count",storageKey:null}],storageKey:null},o={kind:"Variable",name:"storage_host_name",variableName:"storage_host_name"},l=[{kind:"Variable",name:"quota_scope_id",variableName:"project_quota_scope_id"},o],s=[{args:null,kind:"FragmentSpread",name:"UsageProgressFragment_usageFrgmt"}],d=[{kind:"Variable",name:"quota_scope_id",variableName:"user_quota_scope_id"},o],c=[{alias:null,args:null,concreteType:"QuotaDetails",kind:"LinkedField",name:"details",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"usage_bytes",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hard_limit_bytes",storageKey:null}],storageKey:null}];return{fragment:{argumentDefinitions:[e,n,t,a,i],kind:"Fragment",metadata:null,name:"StorageStatusPanelQuery",selections:[r,{condition:"skipQuotaScope",kind:"Condition",passingValue:!1,selections:[{alias:"project_quota_scope",args:l,concreteType:"QuotaScope",kind:"LinkedField",name:"quota_scope",plural:!1,selections:s,storageKey:null},{alias:"user_quota_scope",args:d,concreteType:"QuotaScope",kind:"LinkedField",name:"quota_scope",plural:!1,selections:s,storageKey:null}]}],type:"Queries",abstractKey:null},kind:"Request",operation:{argumentDefinitions:[e,n,i,a,t],kind:"Operation",name:"StorageStatusPanelQuery",selections:[r,{condition:"skipQuotaScope",kind:"Condition",passingValue:!1,selections:[{alias:"project_quota_scope",args:l,concreteType:"QuotaScope",kind:"LinkedField",name:"quota_scope",plural:!1,selections:c,storageKey:null},{alias:"user_quota_scope",args:d,concreteType:"QuotaScope",kind:"LinkedField",name:"quota_scope",plural:!1,selections:c,storageKey:null}]}]},params:{cacheID:"c21e2108cecce6a53eb1fa3c8706b06e",id:null,metadata:{},name:"StorageStatusPanelQuery",operationKind:"query",text:"query StorageStatusPanelQuery(\n  $keypair_resource_policy_name: String\n  $project_quota_scope_id: String!\n  $user_quota_scope_id: String!\n  $storage_host_name: String!\n  $skipQuotaScope: Boolean!\n) {\n  keypair_resource_policy(name: $keypair_resource_policy_name) {\n    max_vfolder_count\n  }\n  project_quota_scope: quota_scope(quota_scope_id: $project_quota_scope_id, storage_host_name: $storage_host_name) @skip(if: $skipQuotaScope) {\n    ...UsageProgressFragment_usageFrgmt\n  }\n  user_quota_scope: quota_scope(quota_scope_id: $user_quota_scope_id, storage_host_name: $storage_host_name) @skip(if: $skipQuotaScope) {\n    ...UsageProgressFragment_usageFrgmt\n  }\n}\n\nfragment UsageProgressFragment_usageFrgmt on QuotaScope {\n  details {\n    usage_bytes\n    hard_limit_bytes\n  }\n}\n"}}}();a.hash="bf52bea1f21e2b4ac3ca5f541bd0d96e",n.default=a},407:function(e,n,t){t.r(n);var a={argumentDefinitions:[],kind:"Fragment",metadata:null,name:"UsageProgressFragment_usageFrgmt",selections:[{alias:null,args:null,concreteType:"QuotaDetails",kind:"LinkedField",name:"details",plural:!1,selections:[{alias:null,args:null,kind:"ScalarField",name:"usage_bytes",storageKey:null},{alias:null,args:null,kind:"ScalarField",name:"hard_limit_bytes",storageKey:null}],storageKey:null}],type:"QuotaScope",abstractKey:null,hash:"1ba87b250f2a0161ecee7ba88d54c85c"};n.default=a},3255:function(e,n,t){t.d(n,{Hz:function(){return l},Lc:function(){return r},Uz:function(){return s},VQ:function(){return d},We:function(){return i},en:function(){return o},lA:function(){return c}});var a=t(2556),i=function(e){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:/(<br\s*\/?>|\n)/;return e.split(n).map((function(e,t){return e.match(n)?(0,a.jsx)("br",{},t):e}))},r=function(e){var n=e.method,t=e.url,a=e.body,i=void 0===a?null:a,r=e.client,o=null===r||void 0===r?void 0:r.newSignedRequest(n,t,i,null);return null===r||void 0===r?void 0:r._wrapWithPromise(o)},o=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2;if(0===e)return"0 Bytes";var t=Math.pow(10,3);n=n<0?0:n;var a=Math.floor(Math.log(Math.round(e))/Math.log(t));return a=a<0?0:a,parseFloat((e/Math.pow(t,a)).toFixed(n))+" "+["Bytes","KB","MB","GB","TB","PB"][a]},l=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:0,n=Math.pow(10,9);return Math.round(n*e)},s=function(e){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:2;return null===e||void 0===e?arguments.length>2&&void 0!==arguments[2]?arguments[2]:"-":e?(e/Math.pow(10,9)).toFixed(n):e},d=function(e,n){return""===n||void 0===n?"":n.startsWith("".concat(e,":"))?n:"".concat(e,":").concat(n)},c=function(e){return e<70?"rgba(58, 178, 97, 1)":e<90?"rgb(223, 179, 23)":"#ef5350"}},7760:function(e,n,t){t.d(n,{Dj:function(){return c},Kr:function(){return o},M:function(){return d},qh:function(){return s},tQ:function(){return l}});var a=t(9439),i=t(4519),r=t(7112),o=function(e){var n=(0,i.useState)(e||(new Date).toISOString()),t=(0,a.Z)(n,2),r=t[0],o=t[1];return[r,function(e){o(e||(new Date).toISOString())}]},l=function(){return c()._config.domainName},s=function(){var e=c(),n=(0,i.useState)({name:e.current_group,id:e.groupIds[e.current_group]}),t=(0,a.Z)(n,2),r=t[0],o=t[1];return(0,i.useEffect)((function(){var n=function(n){var t=n.detail;o({name:t,id:e.groupIds[t]})};return document.addEventListener("backend-ai-group-changed",n),function(){document.removeEventListener("backend-ai-group-changed",n)}})),r},d=function(e){var n=e.api_endpoint;return(0,i.useMemo)((function(){var e=new globalThis.BackendAIClientConfig("","",n,"SESSION");return new globalThis.BackendAIClient(e,"Backend.AI Console.")}),[n])},c=function(){return(0,r.useQuery)({queryKey:"backendai-client-for-suspense",queryFn:function(){return new Promise((function(e){if("undefined"!==typeof globalThis.backendaiclient&&null!==globalThis.backendaiclient&&!1!==globalThis.backendaiclient.ready)return e(globalThis.backendaiclient);document.addEventListener("backend-ai-connected",(function n(){e(globalThis.backendaiclient),document.removeEventListener("backend-ai-connected",n)}))}))},retry:!1,suspense:!0}).data}}}]);
//# sourceMappingURL=588.6d0edf4a.chunk.js.map