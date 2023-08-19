import{_ as i,n as e,b as t,e as n,B as o,c as s,I as a,a as c,m as l,d as r,i as p,ar as h,as as u,g as d,f as g,x as f}from"./backend-ai-webui-d4819018.js";let b=class extends o{constructor(){super(...arguments),this.webUIShell=Object(),this.clientConfig=Object(),this.client=Object(),this.notification=Object()}static get styles(){return[s,a,c,l,r,p`
      `]}firstUpdated(){this.notification=globalThis.lablupNotification}detectIE(){try{return!!!!document.documentMode||(navigator.userAgent.indexOf("MSIE")>0||navigator.userAgent.indexOf("WOW")>0||navigator.userAgent.indexOf(".NET")>0)}catch(i){const e=i.toString();return console.log(e),!1}}async prepareProjectInformation(){const i=`query { user{ ${["email","groups {name, id}"].join(" ")} } }`,e=await globalThis.backendaiclient.query(i,{});globalThis.backendaiclient.groups=e.user.groups.map((i=>i.name)).sort(),globalThis.backendaiclient.groupIds=e.user.groups.reduce(((i,e)=>(i[e.name]=e.id,i)),{});const t=globalThis.backendaiutils._readRecentProjectGroup();globalThis.backendaiclient.current_group=t||globalThis.backendaiclient.groups[0],globalThis.backendaiclient.current_group_id=()=>globalThis.backendaiclient.groupIds[globalThis.backendaiclient.current_group],console.log("current project:",t)}async launch(i){await this._initClient(i);if(await this._token_login()){await this.prepareProjectInformation();const i=window.location.search,e=new URLSearchParams(i),t=e.get("session_id")||null;if(t){const i=e.get("app")||"jupyter";this._openServiceApp(t,i)}else await this._createEduSession()}}async _initClient(i){this.notification=globalThis.lablupNotification;const e=document.querySelector("#webui-shell");if(""===i){const e=localStorage.getItem("backendaiwebui.api_endpoint");null!=e&&(i=e.replace(/^"+|"+$/g,""))}i=i.trim(),this.clientConfig=new h("","",i,"SESSION"),globalThis.backendaiclient=new u(this.clientConfig,"Backend.AI Web UI.");await e._parseConfig("../../config.toml"),globalThis.backendaiclient._config._proxyURL=e.config.wsproxy.proxyURL,await globalThis.backendaiclient.get_manager_version(),globalThis.backendaiclient.ready=!0}async _token_login(){const i=window.location.search,e=new URLSearchParams(i),t=e.get("sToken")||e.get("stoken")||null;null!==t&&(document.cookie=`sToken=${t}; expires=Session; path=/`);const n={};for(const[i,t]of e.entries())"sToken"!==i&&"stoken"!==i&&(n[i]=t);try{if(await globalThis.backendaiclient.check_login())console.log("already logged-in session");else{console.log("logging with (cookie) token...");if(!await globalThis.backendaiclient.token_login(t,n))return this.notification.text=d("eduapi.CannotAuthorizeSessionByToken"),this.notification.show(!0),!1}return!0}catch(i){return this.notification.text=d("eduapi.CannotAuthorizeSessionByToken"),this.notification.show(!0,i),!1}}generateSessionId(){let i="";const e="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";for(let t=0;t<8;t++)i+=e.charAt(Math.floor(62*Math.random()));return i+"-session"}async _createEduSession(){this.appLauncher.indicator=await globalThis.lablupIndicator.start();const i=["session_id","name","access_key","status","status_info","service_ports","mounts"];let e;e=globalThis.backendaiclient.supports("avoid-hol-blocking")?["RUNNING","RESTARTING","TERMINATING","PENDING","SCHEDULED","PREPARING","PULLING"].join(","):["RUNNING","RESTARTING","TERMINATING","PENDING","PREPARING","PULLING"].join(",");const t=globalThis.backendaiclient._config.accessKey;let n;try{this.appLauncher.indicator.set(20,d("eduapi.QueryingExisitingComputeSession")),n=await globalThis.backendaiclient.computeSession.list(i,e,t,30,0)}catch(i){return console.error(i),void(i&&i.message?(i.description?this.notification.text=g.relieve(i.description):this.notification.text=g.relieve(i.message),this.notification.detail=i.message,this.notification.show(!0,i)):i&&i.title&&(this.notification.text=g.relieve(i.title),this.notification.show(!0,i)))}const o=window.location.search;let s,a=new URLSearchParams(o).get("app")||"jupyter",c=!0;if(n.compute_session_list.total_count>0){console.log("Reusing an existing session ...");const i=n.compute_session_list.items[0].status;if("RUNNING"!==i)return this.notification.text=d("eduapi.sessionStatusIs")+` ${i}. `+d("eduapi.PleaseReload"),void this.notification.show(!0);let e=null;for(let i=0;i<n.compute_session_list.items.length;i++){const t=n.compute_session_list.items[i];if(JSON.parse(t.service_ports||"{}").map((i=>i.name)).includes(a)){e=t;break}}e?(c=!1,s="session_id"in e?e.session_id:null,this.appLauncher.indicator.set(50,d("eduapi.FoundExistingComputeSession"))):c=!0,s=null!==e&&"session_id"in e?e.session_id:null}if(c){let i;console.log("Creating a new session ..."),this.appLauncher.indicator.set(40,d("eduapi.FindingSessionTemplate"));try{i=await globalThis.backendaiclient.sessionTemplate.list(!1)}catch(i){return console.error(i),void(i&&i.message?(i.description?this.notification.text=g.relieve(i.description):this.notification.text=g.relieve(i.message),this.notification.detail=i.message,this.notification.show(!0,i)):i&&i.title&&(this.notification.text=g.relieve(i.title),this.notification.show(!0,i)))}if(i=i.filter((i=>i.name===a)),i.length<1)return this.notification.text=d("eduapi.NoSessionTemplate"),void this.notification.show(!0);const e=i[0].id;try{const i=await globalThis.backendaiclient.eduApp.get_mount_folders(),t=i?{mounts:i}:{};let n;try{this.appLauncher.indicator.set(60,d("eduapi.CreatingComputeSession")),n=await globalThis.backendaiclient.createSessionFromTemplate(e,null,null,t,2e4)}catch(i){return console.error(i),void(i&&i.message?(i.description?this.notification.text=g.relieve(i.description):this.notification.text=g.relieve(i.message),this.notification.detail=i.message,this.notification.show(!0,i)):i&&i.title&&(this.notification.text=g.relieve(i.title),this.notification.show(!0,i)))}s=n.sessionId}catch(i){console.error(i),i&&i.message?("statusCode"in i&&408===i.statusCode?this.notification.text=d("eduapi.SessionStillPreparing"):i.description?this.notification.text=g.relieve(i.description):this.notification.text=g.relieve(i.message),this.notification.detail=i.message,this.notification.show(!0,i)):i&&i.title&&(this.notification.text=g.relieve(i.title),this.notification.show(!0,i))}}this.appLauncher.indicator.set(100,d("eduapi.ComputeSessionPrepared")),s&&(a.startsWith("jupyter")&&!this.detectIE()&&(a="jupyterlab"),this._openServiceApp(s,a))}async _openServiceApp(i,e){this.appLauncher.indicator=await globalThis.lablupIndicator.start(),console.log(`launching ${e} from session ${i} ...`),this.appLauncher._open_wsproxy(i,e,null,null).then((async i=>{if(i.url){const e=await this.appLauncher._connectToProxyWorker(i.url,"");this.appLauncher.indicator.set(100,d("session.applauncher.Prepared")),setTimeout((()=>{globalThis.open(e||i.url,"_self")}))}}))}render(){return f`
      <backend-ai-app-launcher id="app-launcher"></backend-ai-app-launcher>
    `}};i([e({type:Object})],b.prototype,"webUIShell",void 0),i([e({type:Object})],b.prototype,"clientConfig",void 0),i([e({type:Object})],b.prototype,"client",void 0),i([e({type:Object})],b.prototype,"notification",void 0),i([t("#app-launcher")],b.prototype,"appLauncher",void 0),b=i([n("backend-ai-edu-applauncher")],b);
