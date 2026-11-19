(() => {
  const main = document.querySelector('main.container');
  if (!main) return;
  const pageHead = main.querySelector(':scope > .page-head');
  const sections = [...main.children].filter(el => el !== pageHead && el.matches('section'));
  if (!sections.length) return;
  const groups = [
    {id:'overview', label:'Overview', match: el => /overview-title|focus-title/i.test(el.getAttribute('aria-labelledby') || '')},
    {id:'assessments', label:'Assessments', match: el => /starting-point-title|style-title|Establish your starting point|Your Manager Style Profile/i.test((el.getAttribute('aria-labelledby') || '') + ' ' + el.innerText.slice(0,180))},
    {id:'capabilities', label:'Capabilities', match: el => /^domain-/.test(el.getAttribute('aria-labelledby') || '')},
    {id:'goals', label:'Goals & actions', match: el => /goals-title|actions-title/i.test(el.getAttribute('aria-labelledby') || '')},
    {id:'review', label:'Development review', match: el => /review-title/i.test(el.getAttribute('aria-labelledby') || '')}
  ];
  const assigned = new Map(groups.map(g => [g.id, []]));
  sections.forEach(section => {
    const group = groups.find(g => g.match(section)) || groups[0];
    assigned.get(group.id).push(section);
  });
  const nav = document.createElement('div');
  nav.className = 'app-tabs'; nav.setAttribute('role','tablist'); nav.setAttribute('aria-label','Manager Blueprint sections');
  const panels = document.createElement('div'); panels.className = 'app-tab-panels';
  groups.forEach((group, index) => {
    const items = assigned.get(group.id); if (!items.length) return;
    const button = document.createElement('button'); button.type='button'; button.role='tab'; button.textContent=group.label;
    button.id=`tab-${group.id}`; button.setAttribute('aria-controls',`panel-${group.id}`); button.setAttribute('aria-selected',String(index===0));
    const panel = document.createElement('section'); panel.className='app-tab-panel'; panel.id=`panel-${group.id}`; panel.role='tabpanel'; panel.setAttribute('aria-labelledby',button.id);
    items.forEach(item => panel.append(item));
    if (index!==0) panel.hidden=true;
    button.addEventListener('click', () => {
      [...nav.children].forEach(tab => tab.setAttribute('aria-selected',String(tab===button)));
      [...panels.children].forEach(p => p.hidden=p!==panel);
    });
    nav.append(button); panels.append(panel);
  });
  if (pageHead) pageHead.after(nav,panels); else main.prepend(nav,panels);
})();
