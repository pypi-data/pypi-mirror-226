"use strict";(self.webpackChunkbackend_ai_webui_react=self.webpackChunkbackend_ai_webui_react||[]).push([[478],{9277:function(e,n,i){var t=i(1413),r=i(4925),o=i(8159),s=(i(4519),i(2556)),l=["direction","wrap","justify","align","gap","style","children"];n.Z=function(e){var n=e.direction,i=void 0===n?"row":n,a=e.wrap,c=void 0===a?"nowrap":a,d=e.justify,u=void 0===d?"flex-start":d,x=e.align,m=void 0===x?"center":x,f=e.gap,b=void 0===f?0:f,h=e.style,j=e.children,g=(0,r.Z)(e,l),Z=o.Z.useToken().token,p=[u,m].map((function(e){var n;switch(e){case"start":n="flex-start";break;case"end":n="flex-end";break;case"between":n="space-between";break;case"around":n="space-around";break;default:n=e}return n})),y=(0,t.Z)({display:"flex",flexDirection:i,flexWrap:c,justifyContent:p[0],alignItems:p[1]},h);return(0,s.jsx)("div",(0,t.Z)((0,t.Z)({style:(0,t.Z)({alignItems:"stretch",backgroundColor:"transparent",border:"0 solid black",boxSizing:"border-box",display:"flex",flexBasis:"auto",flexDirection:"column",flexShrink:0,listStyle:"none",margin:0,minHeight:0,minWidth:0,padding:0,position:"relative",textDecoration:"none",gap:"string"===typeof b?Z["padding"+b.toUpperCase()]:b},y)},g),{},{children:j}))}},478:function(e,n,i){i.r(n);var t=i(3861),r=i(3971),o=i(5658),s=i(5870),l=i(8159),a=i(5492),c=i(2704),d=i(6720),u=i(867),x=i(7171),m=i(1748),f=i(9277),b=i(7112),h=i(3255),j=i(7760),g=i(2556),Z=function(e){var n=e.title,i=e.subtitle;return(0,g.jsxs)(f.Z,{direction:"column",align:"start",children:[(0,g.jsx)(o.Z.Text,{strong:!0,children:n}),i&&(0,g.jsx)(o.Z.Text,{type:"secondary",children:i})]})},p=function(e){var n=e.label,i=e.value;return(0,g.jsxs)(f.Z,{direction:"row",children:[(0,g.jsx)(s.Z,{style:{margin:0,marginRight:-1,zIndex:1},children:n}),(0,g.jsx)(s.Z,{color:"green",children:i})]})};n.default=function(){var e=(0,m.$G)().t,n=l.Z.useToken().token,i=(0,j.Dj)(),o=(0,b.useQuery)("licenseInfo",(function(){return i.enterprise.getLicense()}),{suspense:!1}),y=o.data,k=o.isLoading;y||(y={valid:!1,type:e("information.CannotRead"),licensee:e("information.CannotRead"),key:e("information.CannotRead"),expiration:e("information.CannotRead")});var v={xxl:4,xl:4,lg:2,md:1,sm:1,xs:1};return(0,g.jsxs)(f.Z,{direction:"column",align:"stretch",style:{margin:n.marginSM,gap:n.margin},children:[(0,g.jsxs)(a.Z,{gutter:[n.margin,n.margin],children:[(0,g.jsx)(c.Z,{xs:24,xxl:12,children:(0,g.jsx)(d.Z,{style:{height:"100%"},children:(0,g.jsxs)(u.Z,{title:e("information.Core"),bordered:!0,column:v,children:[(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.ManagerVersion")}),children:(0,g.jsxs)(f.Z,{direction:"column",style:{gap:n.marginXXS},align:"start",children:["Backend.AI ",i.managerVersion,(0,g.jsx)(p,{label:e("information.Installation"),value:i.managerVersion})]})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.APIVersion")}),children:i.apiVersion})]})})}),(0,g.jsx)(c.Z,{xs:24,xxl:12,children:(0,g.jsx)(d.Z,{children:(0,g.jsxs)(u.Z,{title:e("information.Security"),bordered:!0,column:v,children:[(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.DefaultAdministratorAccountChanged"),subtitle:e("information.DescDefaultAdministratorAccountChanged")}),children:(0,g.jsx)(t.Z,{title:"Yes"})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.UsesSSL"),subtitle:e("information.DescUsesSSL")}),children:null!==i&&void 0!==i&&i._config.endpoint.startsWith("https:")?(0,g.jsx)(t.Z,{title:"Yes"}):(0,g.jsx)(r.Z,{style:{color:"red"},title:"No"})})]})})})]}),(0,g.jsx)(d.Z,{children:(0,g.jsxs)(u.Z,{title:e("information.Component"),bordered:!0,column:{xxl:4,xl:2,lg:2,md:1,sm:1,xs:1},children:[(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.DockerVersion"),subtitle:e("information.DescDockerVersion")}),children:(0,g.jsx)(s.Z,{children:e("information.Compatible")})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.PostgreSQLVersion"),subtitle:e("information.DescPostgreSQLVersion")}),children:(0,g.jsx)(s.Z,{children:e("information.Compatible")})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.ETCDVersion"),subtitle:e("information.DescETCDVersion")}),children:(0,g.jsx)(s.Z,{children:e("information.Compatible")})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.RedisVersion"),subtitle:(0,h.W)(e("information.DescRedisVersion"))}),children:(0,g.jsx)(s.Z,{children:e("information.Compatible")})})]})}),(0,g.jsx)(d.Z,{children:(0,g.jsx)(x.Z,{spinning:k,children:(0,g.jsxs)(u.Z,{title:e("information.License"),bordered:!0,column:{xxl:2,xl:2,lg:2,md:1,sm:1,xs:1},children:[(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.IsLicenseValid"),subtitle:e("information.DescIsLicenseValid")}),children:y.valid?(0,g.jsx)(t.Z,{}):(0,g.jsx)(r.Z,{style:{color:"red"}})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.LicenseType"),subtitle:(0,h.W)(e("information.DescLicenseType"))}),children:(0,g.jsx)(s.Z,{children:"fixed"===y.type?e("information.FixedLicense"):e("information.DynamicLicense")})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.Licensee"),subtitle:e("information.DescLicensee")}),children:(0,g.jsx)(s.Z,{children:y.licensee})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.LicenseKey"),subtitle:e("information.DescLicenseKey")}),children:(0,g.jsx)(s.Z,{children:y.key})}),(0,g.jsx)(u.Z.Item,{label:(0,g.jsx)(Z,{title:e("information.Expiration"),subtitle:e("information.DescExpiration")}),children:(0,g.jsx)(s.Z,{children:y.expiration})})]})})})]})}},3255:function(e,n,i){i.d(n,{L:function(){return o},W:function(){return r}});var t=i(2556),r=function(e){var n=arguments.length>1&&void 0!==arguments[1]?arguments[1]:/(<br\s*\/?>|\n)/;return e.split(n).map((function(e,i){return e.match(n)?(0,t.jsx)("br",{},i):e}))},o=function(e){var n=e.method,i=e.url,t=e.body,r=void 0===t?null:t,o=e.client,s=o.newSignedRequest(n,i,r,null);return o._wrapWithPromise(s)}},7760:function(e,n,i){i.d(n,{Dj:function(){return s},M:function(){return o}});var t=i(4519),r=i(7112),o=function(e){var n=e.api_endpoint;return(0,t.useMemo)((function(){var e=new globalThis.BackendAIClientConfig("","",n,"SESSION");return new globalThis.BackendAIClient(e,"Backend.AI Console.")}),[n])},s=function(){return(0,r.useQuery)({queryKey:"backendai-client-for-suspense",queryFn:function(){return new Promise((function(e){if("undefined"!==typeof globalThis.backendaiclient&&null!==globalThis.backendaiclient&&!1!==globalThis.backendaiclient.ready)return e(globalThis.backendaiclient);document.addEventListener("backend-ai-connected",(function n(){e(globalThis.backendaiclient),document.removeEventListener("backend-ai-connected",n)}))}))},retry:!1,suspense:!0}).data}}}]);
//# sourceMappingURL=478.8c8fd27b.chunk.js.map