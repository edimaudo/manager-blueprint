(() => {
  const root = document.getElementById('style-quiz');
  const out = document.getElementById('style-result');
  if (!root || !out) return;
  const allowed = root.dataset.allowed === 'true';
  async function loadQuestions() {
    try {
      const response = await fetch('/api/style/questions');
      const data = await response.json();
      if (!response.ok || !data.questions) throw new Error(data.detail || 'Unable to load the assessment.');
      root.replaceChildren();
      if (!allowed) {
        const message = document.createElement('p');
        message.textContent = `You can retake this reflection on or after ${root.dataset.nextAllowed || 'the next eligible date'}. Your previous results remain available below.`;
        root.append(message);
        return;
      }
      const form = document.createElement('form'); form.id = 'style-form';
      data.questions.forEach(question => {
        const field = document.createElement('fieldset'); field.className = 'question';
        const legend = document.createElement('legend'); legend.textContent = `${question.id}. ${question.question}`; field.append(legend);
        question.options.forEach(option => {
          const label = document.createElement('label'); label.className = 'choice';
          const input = document.createElement('input'); input.type = 'radio'; input.name = String(question.id); input.value = option.value; input.required = true;
          label.append(input, document.createTextNode(option.label)); field.append(label);
        });
        form.append(field);
      });
      const button = document.createElement('button'); button.className = 'button'; button.type = 'submit'; button.textContent = 'Generate my archetype'; form.append(button);
      form.addEventListener('submit', submitForm);
      root.append(form);
    } catch (error) { root.textContent = error.message; }
  }
  async function submitForm(event) {
    event.preventDefault(); const form = event.currentTarget; const button = form.querySelector('button'); button.disabled = true;
    const values = new FormData(form); const answers = {};
    for (let i = 1; i <= 12; i++) answers[String(i)] = values.get(String(i));
    if (Object.values(answers).some(value => !value)) { button.disabled = false; return; }
    try {
      const response = await fetch('/api/style/submit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answers }) });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || 'Unable to save assessment.');
      renderResult(payload.result);
      root.dataset.allowed = 'false';
      form.replaceWith(Object.assign(document.createElement('p'), { textContent: 'Your reflection has been saved. It can be retaken after the 90-day interval.' }));
      out.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) { const note = document.createElement('p'); note.className = 'error'; note.textContent = error.message; form.prepend(note); }
    finally { button.disabled = false; }
  }
  function renderResult(result) {
    out.replaceChildren(); out.hidden = false;
    const title = document.createElement('h2'); title.textContent = result.archetype;
    const summary = document.createElement('p'); summary.textContent = result.profile_summary || '';
    const addList = (heading, values) => {
      const h = document.createElement('h3'); h.textContent = heading; out.append(h);
      const ul = document.createElement('ul'); (values || []).forEach(value => { const li = document.createElement('li'); li.textContent = value; ul.append(li); }); out.append(ul);
    };
    out.append(title, summary);
    addList('Potential strengths', result.strengths);
    const watch = document.createElement('p'); watch.textContent = `Watch-outs: ${result.watchouts}`;
    const coaching = document.createElement('p'); coaching.textContent = `Coaching approach: ${result.coaching_approach}`;
    out.append(watch, coaching);
    const approach = document.createElement('p'); approach.textContent = `Management approach to try: ${result.management_approach || result.coaching_approach}`;
    out.append(approach);
    addList('Potential weaknesses and watch-outs', result.potential_weaknesses || [result.watchouts]);
    addList('Management adjustments to consider', result.management_adjustments);
    const scoreSection = document.createElement('div');
    const scoreHeading = document.createElement('h3'); scoreHeading.textContent = 'Reflection score patterns'; scoreSection.append(scoreHeading);
    const addScores = (label, values) => {
      const heading = document.createElement('p'); heading.textContent = label; scoreSection.append(heading);
      Object.entries(values || {}).forEach(([key, value]) => {
        const row = document.createElement('div'); row.className = 'score-row';
        const name = document.createElement('span'); name.textContent = key.toUpperCase();
        const track = document.createElement('div'); track.className = 'progress';
        const fill = document.createElement('span'); fill.style.width = `${value}%`; track.append(fill);
        const amount = document.createElement('small'); amount.textContent = `${value}%`;
        row.append(name, track, amount); scoreSection.append(row);
      });
    };
    addScores('Behavioral preferences', result.disc_percentages);
    addScores('Contribution domains', result.strength_domain_percentages);
    out.append(scoreSection);
    const note = document.createElement('p'); note.className = 'muted'; note.textContent = result.disclaimer; out.append(note);
  }
  loadQuestions();
})();
