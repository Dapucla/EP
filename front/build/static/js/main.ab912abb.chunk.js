(this.webpackJsonpfront=this.webpackJsonpfront||[]).push([[0],{22:function(e,c,t){},23:function(e,c,t){},42:function(e,c,t){},44:function(e,c,t){"use strict";t.r(c);var n=t(2),s=t.n(n),a=t(12),i=t.n(a),l=(t(22),t(13)),o=t(14),r=t(17),d=t(16),j=(t.p,t(23),t(15)),h=t.n(j),u=(t(42),t(0)),b=function(e){Object(r.a)(t,e);var c=Object(d.a)(t);function t(){var e;Object(l.a)(this,t);for(var n=arguments.length,s=new Array(n),a=0;a<n;a++)s[a]=arguments[a];return(e=c.call.apply(c,[this].concat(s))).state={categories:[]},e}return Object(o.a)(t,[{key:"componentDidMount",value:function(){var e,c=this;h.a.get("http://127.0.0.1:8000/api/smartphones/").then((function(t){e=t.data,c.setState({categories:e})})).catch((function(e){})),console.log(this.state.categories)}},{key:"render",value:function(){return Object(u.jsx)("div",{className:"App",children:Object(u.jsx)("div",{className:"contact",children:Object(u.jsxs)("ul",{className:"responsive-table",children:[Object(u.jsxs)("li",{className:"table-header",children:[Object(u.jsx)("div",{className:"col col-1",children:"Id"}),Object(u.jsx)("div",{className:"col col-2",children:"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435"}),Object(u.jsx)("div",{className:"col col-3",children:"\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435"}),Object(u.jsx)("div",{className:"col col-4",children:"\u0426\u0435\u043d\u0430"})]}),this.state.categories.map((function(e){return Object(u.jsxs)("li",{className:"table-row",children:[Object(u.jsx)("div",{className:"col col-1",children:e.id}),Object(u.jsx)("div",{className:"col col-2",children:e.title}),Object(u.jsx)("div",{className:"col col-3",children:e.description}),Object(u.jsx)("div",{className:"col col-4",children:e.price})]},e.id)}))]})})})}}]),t}(s.a.Component),m=function(e){e&&e instanceof Function&&t.e(3).then(t.bind(null,45)).then((function(c){var t=c.getCLS,n=c.getFID,s=c.getFCP,a=c.getLCP,i=c.getTTFB;t(e),n(e),s(e),a(e),i(e)}))};i.a.render(Object(u.jsx)(s.a.StrictMode,{children:Object(u.jsx)(b,{})}),document.getElementById("root")),m()}},[[44,1,2]]]);
//# sourceMappingURL=main.ab912abb.chunk.js.map