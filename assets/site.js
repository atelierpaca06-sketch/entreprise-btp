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
      if(j.success){res.className='res ok';res.textContent='Demande envoyée. Nous vous rappelons sous 2 h en journée (7 j/7 pour les urgences).';f.reset();}
      else throw new Error();
    }).catch(function(){res.className='res ko';res.textContent='L’envoi a échoué. Appelez-nous directement au 04 92 14 14 14.';})
    .finally(function(){btn.disabled=false;btn.textContent=t;});
  });}
})();
