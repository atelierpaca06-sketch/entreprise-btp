/* Atelier PACA — comportements légers : menu mobile, formulaire devis, marquage nav */
(function(){
  var b=document.getElementById('burger'),m=document.getElementById('menu-m');
  if(b&&m){b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');document.body.style.overflow=o?'hidden':'';});}
  var f=document.getElementById('devis-form');
  if(f){f.addEventListener('submit',function(e){
    e.preventDefault();
    if(f.querySelector('[name=botcheck]')&&f.querySelector('[name=botcheck]').checked)return;
    var btn=f.querySelector('button[type=submit]'),res=f.querySelector('.res'),t=btn.textContent;
    btn.disabled=true;btn.textContent='Envoi en cours…';res.className='res';
    fetch('https://api.web3forms.com/submit',{method:'POST',body:new FormData(f),headers:{'Accept':'application/json'}})
    .then(function(r){return r.json()}).then(function(j){
      if(j.success){res.className='res ok';res.textContent='Demande envoyée. Nous vous rappelons sous 2 h en journée (7 j/7 pour les urgences).';f.reset();f.dispatchEvent(new Event('devis-ok'));}
      else throw new Error();
    }).catch(function(){res.className='res ko';res.textContent='L’envoi a échoué. Appelez-nous directement au 04 92 14 14 14.';})
    .finally(function(){btn.disabled=false;btn.textContent=t;});
  });}

  /* ---- Google Analytics 4 : chargé seulement après « Accepter » (consentement CNIL) ---- */
  var ga=document.documentElement.getAttribute('data-ga4'),ck=document.getElementById('cookie');
  if(ga&&ck){
    var K='ap_consent',now=Date.now(),c=null;
    try{c=JSON.parse(localStorage.getItem(K)||'null');}catch(e){}
    if(c&&c.exp<now)c=null;
    window.dataLayer=window.dataLayer||[];
    function gtag(){dataLayer.push(arguments);}
    window.gtag=gtag;
    gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});
    function load(){
      gtag('consent','update',{analytics_storage:'granted'});
      var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id='+ga;document.head.appendChild(s);
      gtag('js',new Date());gtag('config',ga,{anonymize_ip:true});
      /* Conversions : appel, WhatsApp, devis envoyé */
      document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'';
        if(h.indexOf('tel:')===0)gtag('event','appel',{event_category:'contact',event_label:location.pathname});
        else if(h.indexOf('wa.me')>-1)gtag('event','whatsapp',{event_category:'contact',event_label:location.pathname});});
      if(f)f.addEventListener('devis-ok',function(){gtag('event','devis',{event_category:'contact',event_label:location.pathname});});
    }
    function save(v){try{localStorage.setItem(K,JSON.stringify({v:v,exp:now+(v==='ok'?395:182)*864e5}));}catch(e){}ck.classList.remove('show');}
    if(c&&c.v==='ok')load();
    else if(!c){ck.classList.add('show');
      document.getElementById('ck-ok').addEventListener('click',function(){save('ok');load();});
      document.getElementById('ck-no').addEventListener('click',function(){save('no');});}
  }
})();
