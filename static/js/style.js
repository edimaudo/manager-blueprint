(() => {
  const root = document.getElementById('style-quiz');
  const out = document.getElementById('style-result');
  if (!root || !out) return;
  let questions = [];
  const sectionLabels = {
    behaviour: 'Behavioural preferences',
    contribution: 'Contribution patterns'
  };

  async function loadQuestions() {
    try {
      const response = await fetch('/api/style/questions');
      const data = await response.json();
      if (!response.ok || !Array.isArray(data.questions) || !Array.isArray(data.scale)) {
        throw new Error(data.detail || 'Unable to load the assessment.');
      }
      questions = data.questions;
      root.replaceChildren();
      if (root.dataset.allowed !== 'true') {
        const message = document.createElement('p');
        message.textContent = `You can retake this profile on or after ${root.dataset.nextAllowed || 'the next eligible date'}. Your previous results remain available below.`;
        root.append(message);
        return;
      }

      const form = document.createElement('form');
      form.id = 'style-form';
      form.noValidate = true;
      const instructions = document.createElement('p');
      instructions.textContent = `${data.question_count} original statements. Four statements contribute to each of eight dimensions. For each one, choose how accurately it describes your usual approach as a manager. There are no right or wrong answers.`;
      form.append(instructions);
      const tabs = document.createElement('div');
      tabs.className = 'assessment-domain-tabs';
      tabs.setAttribute('role', 'tablist');
      tabs.setAttribute('aria-label', 'Manager Style Profile sections');
      const sectionPanels = {};
      ['behaviour', 'contribution'].forEach((section, index) => {
        const tab = document.createElement('button');
        tab.type = 'button'; tab.setAttribute('role', 'tab');
        tab.setAttribute('aria-selected', String(index === 0));
        tab.textContent = sectionLabels[section];
        tab.addEventListener('click', () => {
          Object.entries(sectionPanels).forEach(([key, panel]) => panel.hidden = key !== section);
          [...tabs.children].forEach(item => item.setAttribute('aria-selected', String(item === tab)));
        });
        tabs.append(tab);
        const panel = document.createElement('section');
        panel.className = 'style-assessment-panel';
        panel.hidden = index !== 0;
        sectionPanels[section] = panel;
        form.append(panel);
      });
      form.insertBefore(tabs, form.children[1]);

      ['behaviour', 'contribution'].forEach(section => {
        const panel = sectionPanels[section];
        const heading = document.createElement('h2');
        heading.className = 'style-section-heading';
        heading.textContent = sectionLabels[section];
        panel.append(heading);
        questions.forEach(question => {
          if (question.section !== section) return;
          const field = document.createElement('fieldset');
          field.className = 'question style-question';
          const legend = document.createElement('legend');
          legend.textContent = `${question.id}. ${question.question}`;
          field.append(legend);
          const label = document.createElement('label');
          label.className = 'visually-hidden';
          label.htmlFor = `style-answer-${question.id}`;
          label.textContent = `Response to statement ${question.id}`;
          const select = document.createElement('select');
          select.id = `style-answer-${question.id}`;
          select.name = String(question.id);
          select.required = true;
          const placeholder = document.createElement('option');
          placeholder.value = '';
          placeholder.textContent = 'Choose a response';
          placeholder.selected = true;
          select.append(placeholder);
          data.scale.forEach(option => {
            const item = document.createElement('option');
            item.value = option.value;
            item.textContent = option.label;
            select.append(item);
          });
          field.append(label, select);
          panel.append(field);
        });
      });

      const consentWrap = document.createElement('div');
      consentWrap.className = 'field';
      const consentLabel = document.createElement('label');
      const consent = document.createElement('input');
      consent.type = 'checkbox';
      consent.name = 'pilot_consent';
      consent.value = 'yes';
      consentLabel.append(consent, document.createTextNode(' I agree to let Manager Blueprint use my de-identified answers in aggregate assessment-quality analysis. This is optional and does not affect my profile.'));
      consentWrap.append(consentLabel);
      form.append(consentWrap);

      const button = document.createElement('button');
      button.className = 'button';
      button.type = 'submit';
      button.textContent = 'Generate my management style';
      form.append(button);
      form.addEventListener('submit', submitForm);
      root.append(form);
    } catch (error) {
      root.textContent = error.message;
    }
  }

  async function submitForm(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    const values = new FormData(form);
    const missing = questions.find(question => !values.get(String(question.id)));
    if (missing) {
      const section = missing.section;
      const panels = [...form.querySelectorAll('.style-assessment-panel')];
      panels.forEach(panel => panel.hidden = panel !== panels[['behaviour','contribution'].indexOf(section)]);
      const tabs = [...form.querySelectorAll('[role="tab"]')];
      tabs.forEach((tab, index) => tab.setAttribute('aria-selected', String(index === ['behaviour','contribution'].indexOf(section))));
      const field = form.querySelector(`#style-answer-${missing.id}`);
      field?.focus();
      button.disabled = false;
      const note = document.createElement('p'); note.className = 'error';
      note.textContent = 'Complete every statement in both sections before generating your profile.';
      form.prepend(note);
      return;
    }
    const answers = {};
    questions.forEach(question => { answers[String(question.id)] = values.get(String(question.id)); });
    if (Object.values(answers).length !== questions.length || Object.values(answers).some(value => !value)) {
      button.disabled = false;
      const note = document.createElement('p');
      note.className = 'error';
      note.textContent = 'Complete every statement before generating your profile.';
      form.prepend(note);
      return;
    }
    try {
      const response = await fetch('/api/style/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers, pilot_consent: values.get('pilot_consent') === 'yes' })
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || 'Unable to save your profile.');
      renderResult(payload.result);
      root.dataset.allowed = 'false';
      const note = document.createElement('p');
      note.textContent = 'Your profile has been saved. It can be retaken after the 90-day interval.';
      form.replaceWith(note);
      out.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } catch (error) {
      const note = document.createElement('p');
      note.className = 'error';
      note.textContent = error.message;
      form.prepend(note);
    } finally {
      button.disabled = false;
    }
  }

  function renderResult(result) {
    out.replaceChildren();
    out.hidden = false;
    const title = document.createElement('h2');
    title.textContent = result.archetype;
    const summary = document.createElement('p');
    summary.textContent = result.profile_summary || '';
    out.append(title, summary);

    const addList = (heading, values) => {
      const h = document.createElement('h3');
      h.textContent = heading;
      out.append(h);
      const ul = document.createElement('ul');
      (values || []).forEach(value => {
        const li = document.createElement('li');
        li.textContent = value;
        ul.append(li);
      });
      out.append(ul);
    };
    addList('Potential strengths', result.strengths);
    addList('Potential blind spots', result.potential_weaknesses);
    const coaching = document.createElement('p');
    coaching.textContent = `Coaching approach: ${result.coaching_approach || ''}`;
    const approach = document.createElement('p');
    approach.textContent = `Management approach: ${result.management_approach || ''}`;
    out.append(coaching, approach);
    addList('Management adjustments to consider', result.management_adjustments);

    const scoreSection = document.createElement('div');
    const scoreHeading = document.createElement('h3');
    scoreHeading.textContent = 'Your profile scores';
    scoreSection.append(scoreHeading);
    const addScores = (heading, values, labels) => {
      const h = document.createElement('h4');
      h.textContent = heading;
      scoreSection.append(h);
      Object.entries(values || {}).forEach(([key, value]) => {
        const row = document.createElement('div');
        row.className = 'score-row';
        const name = document.createElement('span');
        name.textContent = (labels || {})[key] || key;
        const track = document.createElement('div');
        track.className = 'progress';
        track.setAttribute('role', 'progressbar');
        track.setAttribute('aria-valuemin', '0');
        track.setAttribute('aria-valuemax', '100');
        track.setAttribute('aria-valuenow', String(value));
        track.setAttribute('aria-label', `${name.textContent} score`);
        const fill = document.createElement('span');
        fill.style.width = `${value}%`;
        track.append(fill);
        const amount = document.createElement('small');
        amount.textContent = `${value}/100`;
        row.append(name, track, amount);
        scoreSection.append(row);
      });
    };
    addScores('Behavioural preferences', result.disc_percentages, result.disc_labels);
    addScores('Contribution patterns', result.strength_domain_percentages, result.strength_domain_labels);
    out.append(scoreSection);

    const method = document.createElement('p');
    method.className = 'muted';
    method.textContent = result.scoring_method || '';
    const note = document.createElement('p');
    note.className = 'muted';
    note.textContent = result.disclaimer || '';
    out.append(method, note);
  }

  loadQuestions();
})();
