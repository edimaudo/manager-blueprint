(() => {
  const form=document.querySelector('form[action="/onboarding/assessment"]'); if(!form) return;
  const tabs=[...document.querySelectorAll('[data-domain-tab]')];
  const fields=[...form.querySelectorAll('[data-assessment-domain]')];
  const count=document.getElementById('assessment-count');
  const fill=document.getElementById('assessment-progress-fill');
  const progress=fill?.parentElement;
  function updateCount(){
    const answered=fields.filter(f=>f.querySelector('input:checked')).length;
    const total=fields.length;
    if(count) count.textContent=`${answered} of ${total} answered`;
    if(fill) fill.style.width=`${total?answered/total*100:0}%`;
    if(progress) progress.setAttribute('aria-valuenow',String(answered));
  }
  function activate(domain){
    fields.forEach(field=>{field.hidden=field.dataset.assessmentDomain!==domain;});
    tabs.forEach(tab=>tab.setAttribute('aria-selected',String(tab.dataset.domainTab===domain)));
    updateCount();
  }
  tabs.forEach(tab=>tab.addEventListener('click',()=>activate(tab.dataset.domainTab)));
  form.addEventListener('change',updateCount);
  const submit=form.querySelector('button[type="submit"]');
  form.addEventListener('submit',event=>{
    const missing=fields.find(field=>!field.querySelector('input:checked'));
    if(missing){
      event.preventDefault(); activate(missing.dataset.assessmentDomain);
      missing.scrollIntoView({behavior:'smooth',block:'center'});
      const first=missing.querySelector('input'); first?.focus();
    }
  });
  activate(tabs[0]?.dataset.domainTab || fields[0]?.dataset.assessmentDomain);
})();
