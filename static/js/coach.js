(() => {
  const quizBox = document.getElementById('coach-quiz');
  const recommendation = document.getElementById('coach-recommendation');
  const form = document.getElementById('coach-form');
  const conversation = document.getElementById('conversation');
  const messageInput = document.getElementById('message');
  const modeSelect = document.getElementById('mode');
  const capabilitySelect = document.getElementById('capability');
  const scenarioSelect = document.getElementById('scenario');
  const difficultySelect = document.getElementById('difficulty');
  const sessionSelect = document.getElementById('saved-sessions');
  const debriefButton = document.getElementById('debrief');
  const repeatButton = document.getElementById('repeat-scenario');
  const newSessionButton = document.getElementById('new-session');
  const debriefPanel = document.getElementById('practice-debrief');
  const criteriaPanel = document.getElementById('scenario-criteria-panel');
  const criteriaList = document.getElementById('scenario-criteria');
  if (!quizBox || !form) return;

  let activeSessionId = null;
  let activeAttemptId = null;
  let activeAttemptStatus = null;
  let parentAttemptId = difficultySelect?.dataset.parentAttempt || null;
  let isBusy = false;
  const scenarioMap = {};
  [...scenarioSelect.options].forEach(option => {
    if (option.value) scenarioMap[option.value] = option.textContent;
  });

  function addMessage(role, content) {
    const node = document.createElement('article');
    node.className = role === 'user' ? 'chat-user' : 'chat-coach';
    const heading = document.createElement('strong');
    heading.textContent = role === 'user' ? 'You' : 'Your coach';
    const text = document.createElement('p');
    text.textContent = content;
    text.style.whiteSpace = 'pre-wrap';
    text.style.margin = '.35rem 0 0';
    node.append(heading, text);
    conversation.append(node);
    conversation.scrollTop = conversation.scrollHeight;
  }

  function addText(parent, tag, value, className = '') {
    const node = document.createElement(tag);
    node.textContent = value || '';
    if (className) node.className = className;
    parent.append(node);
    return node;
  }

  async function parseResponse(response) {
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || 'The request could not be completed.');
    return data;
  }

  function renderDebrief(debrief) {
    debriefPanel.replaceChildren();
    if (!debrief || typeof debrief !== 'object' || !Object.keys(debrief).length) {
      debriefPanel.hidden = true;
      repeatButton.hidden = true;
      return;
    }
    debriefPanel.hidden = false;
    addText(debriefPanel, 'h3', 'Practice debrief');
    addText(debriefPanel, 'p', debrief.overall_summary || 'The practice has been reviewed.');
    if (debrief.overall_score !== null && debrief.overall_score !== undefined) {
      addText(debriefPanel, 'p', `Overall scenario rating: ${debrief.overall_score} / 5`, 'debrief-score');
    }
    if (Array.isArray(debrief.criteria) && debrief.criteria.length) {
      addText(debriefPanel, 'h4', 'Evaluation criteria');
      const table = document.createElement('table');
      const thead = document.createElement('thead');
      const headRow = document.createElement('tr');
      ['Criterion', 'Rating', 'Evidence'].forEach(label => addText(headRow, 'th', label));
      thead.append(headRow); table.append(thead);
      const tbody = document.createElement('tbody');
      debrief.criteria.forEach(item => {
        const row = document.createElement('tr');
        addText(row, 'td', item.name);
        addText(row, 'td', item.score === null || item.score === undefined ? 'Not enough evidence' : `${item.score} / 5`);
        addText(row, 'td', item.evidence || 'No specific evidence recorded.');
        tbody.append(row);
      });
      table.append(tbody); debriefPanel.append(table);
    }
    [
      ['What worked', 'strengths'],
      ['Development opportunities', 'improvement_areas'],
      ['Alternative language to try', 'stronger_language'],
      ['Suggested next actions', 'next_actions']
    ].forEach(([heading, key]) => {
      if (!Array.isArray(debrief[key]) || !debrief[key].length) return;
      addText(debriefPanel, 'h4', heading);
      const list = document.createElement('ul');
      debrief[key].forEach(item => addText(list, 'li', item));
      debriefPanel.append(list);
    });
    if (debrief.reflection_question) addText(debriefPanel, 'p', `Reflection: ${debrief.reflection_question}`);
    repeatButton.hidden = !(activeAttemptId && activeAttemptStatus === 'debriefed');
  }

  async function refreshSessions() {
    const data = await parseResponse(await fetch('/api/coach/sessions'));
    const selected = activeSessionId;
    sessionSelect.innerHTML = '<option value="">New session</option>';
    data.sessions.forEach(session => {
      const option = document.createElement('option');
      option.value = session.id;
      const difficulty = session.scenario_slug ? ` · ${session.difficulty || 'applied'}` : '';
      option.textContent = `${session.title} · ${String(session.updated_at || '').slice(0, 10)}${difficulty}`;
      sessionSelect.append(option);
    });
    if (selected) sessionSelect.value = selected;
  }

  async function loadSession(sessionId) {
    const data = await parseResponse(await fetch(`/api/coach/sessions/${encodeURIComponent(sessionId)}`));
    activeSessionId = data.session.id;
    sessionSelect.value = activeSessionId;
    capabilitySelect.value = data.session.capability || 'general';
    modeSelect.value = data.session.mode || 'coach';
    scenarioSelect.value = data.session.scenario_slug || '';
    difficultySelect.value = data.session.difficulty || 'applied';
    activeAttemptId = data.practice_attempt?.id || null;
    activeAttemptStatus = data.practice_attempt?.status || null;
    parentAttemptId = null;
    conversation.replaceChildren();
    data.messages.forEach(item => addMessage(item.role, item.content));
    renderDebrief(data.practice_attempt?.debrief || null);
    debriefButton.hidden = !(activeAttemptId && activeAttemptStatus === 'in_progress');
    difficultySelect.disabled = Boolean(activeAttemptId);
    updateScenarioDescription();
  }

  function updateScenarioDescription() {
    const selected = scenarioSelect.value;
    const option = selected ? scenarioSelect.selectedOptions[0] : null;
    const description = document.getElementById('scenario-description');
    const difficultyOption = difficultySelect.selectedOptions[0];
    if (!selected || !option) {
      description.textContent = 'Choose a scenario to practise a realistic management situation with your coach.';
      criteriaPanel.hidden = true;
      criteriaList.replaceChildren();
      return;
    }
    const difficultyDescription = difficultyOption?.dataset.description || '';
    description.textContent = `${option.textContent}. ${difficultyDescription} The coach will play the counterpart and then evaluate observable behaviour against the displayed criteria.`;
    capabilitySelect.value = option.dataset.capability || capabilitySelect.value;
    criteriaList.replaceChildren();
    try {
      const criteria = JSON.parse(option.dataset.criteria || '[]');
      criteria.forEach(item => {
        const li = document.createElement('li');
        const strong = document.createElement('strong');
        strong.textContent = `${item.name}: `;
        li.append(strong, document.createTextNode(item.focus));
        criteriaList.append(li);
      });
      criteriaPanel.hidden = !criteria.length;
    } catch (error) {
      criteriaPanel.hidden = true;
      criteriaList.replaceChildren();
    }
  }

  async function sendMessage(text, modeOverride = null) {
    if (isBusy || !text.trim()) return;
    isBusy = true;
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    const mode = modeOverride || modeSelect.value;
    addMessage('user', text);
    try {
      const data = await parseResponse(await fetch('/api/coach', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          capability: capabilitySelect.value,
          mode,
          scenario_slug: scenarioSelect.value || null,
          difficulty: difficultySelect.value,
          parent_attempt_id: activeSessionId ? null : parentAttemptId,
          session_id: activeSessionId
        })
      }));
      activeSessionId = data.session_id;
      if (data.practice_attempt_id) { activeAttemptId = data.practice_attempt_id; activeAttemptStatus = data.practice_debrief ? 'debriefed' : 'in_progress'; }
      if (data.practice_debrief) { activeAttemptStatus = 'debriefed'; modeSelect.value = 'feedback'; }
      if (parentAttemptId) parentAttemptId = null;
      addMessage('model', data.answer);
      renderDebrief(data.practice_debrief);
      await refreshSessions();
      debriefButton.hidden = !(activeAttemptId && activeAttemptStatus === 'in_progress');
      difficultySelect.disabled = Boolean(activeAttemptId);
    } catch (error) {
      addMessage('model', `The request was not completed: ${error.message}`);
    } finally {
      isBusy = false;
      submitButton.disabled = false;
    }
  }

  async function initQuiz() {
    try {
      const data = await parseResponse(await fetch('/api/coach/quiz'));
      quizBox.replaceChildren();
      const f = document.createElement('form');
      f.id = 'coach-quiz-form';
      data.questions.forEach(question => {
        const field = document.createElement('fieldset'); field.className = 'question';
        const legend = document.createElement('legend'); legend.textContent = `${question.id}. ${question.question}`; field.append(legend);
        question.options.forEach(option => {
          const label = document.createElement('label'); label.className = 'choice';
          const input = document.createElement('input'); input.type = 'radio'; input.name = String(question.id); input.value = option.value; input.required = true;
          label.append(input, document.createTextNode(option.label)); field.append(label);
        });
        f.append(field);
      });
      const button = document.createElement('button'); button.className = 'button'; button.type = 'submit'; button.textContent = 'Recommend my coach'; f.append(button);
      f.addEventListener('submit', async event => {
        event.preventDefault(); button.disabled = true;
        const fd = new FormData(f); const answers = {};
        for (let i = 1; i <= 5; i++) answers[String(i)] = Number(fd.get(String(i)));
        try {
          const result = await parseResponse(await fetch('/api/coach/quiz', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ answers }) }));
          recommendation.replaceChildren();
          addText(recommendation, 'h3', result.recommended_coach);
          addText(recommendation, 'p', result.reasoning);
          addText(recommendation, 'p', result.approach);
          if (Array.isArray(result.supporting_preferences) && result.supporting_preferences.length > 1) {
            addText(recommendation, 'p', `Also present: ${result.supporting_preferences.filter(name => name !== result.recommended_coach).join(', ')}.`, 'muted');
          }
          const scoreHeading = addText(recommendation, 'h4', 'Your preference pattern');
          Object.entries(result.scores || {}).forEach(([name, score]) => {
            const row = document.createElement('div'); row.className = 'score-row';
            addText(row, 'span', name);
            const track = document.createElement('div'); track.className = 'progress';
            const bar = document.createElement('span'); bar.style.width = `${Number(score) / 5 * 100}%`; track.append(bar);
            addText(row, 'small', `${score}/5`); row.insertBefore(track, row.lastChild);
            recommendation.append(row);
          });
        } catch (error) { recommendation.textContent = error.message; }
        finally { button.disabled = false; }
      });
      quizBox.append(f);
    } catch (error) { quizBox.textContent = `Coach preferences are unavailable: ${error.message}`; }
  }

  form.addEventListener('submit', event => {
    event.preventDefault();
    const text = messageInput.value.trim();
    messageInput.value = '';
    sendMessage(text);
  });
  debriefButton.addEventListener('click', () => sendMessage('Pause the role-play and evaluate how I handled the conversation. Use the displayed scenario criteria and provide evidence for each rating.', 'feedback'));
  repeatButton.addEventListener('click', () => {
    if (!activeAttemptId || !scenarioSelect.value) return;
    parentAttemptId = activeAttemptId;
    activeSessionId = null;
    activeAttemptId = null;
    activeAttemptStatus = null;
    sessionSelect.value = '';
    conversation.replaceChildren();
    debriefPanel.hidden = true;
    debriefPanel.replaceChildren();
    repeatButton.hidden = true;
    debriefButton.hidden = true;
    modeSelect.value = 'roleplay';
    difficultySelect.disabled = false;
    messageInput.value = '';
    messageInput.placeholder = 'Begin the scenario in your own words. The counterpart will respond at the selected difficulty.';
    addMessage('model', 'You are starting a new attempt linked to your previous practice. Use the same difficulty to make the comparison more meaningful.');
    messageInput.focus();
  });
  newSessionButton.addEventListener('click', () => {
    activeSessionId = null; activeAttemptId = null; activeAttemptStatus = null; parentAttemptId = null;
    sessionSelect.value = ''; conversation.replaceChildren(); debriefPanel.hidden = true; debriefPanel.replaceChildren();
    debriefButton.hidden = true; repeatButton.hidden = true; difficultySelect.disabled = false;
    messageInput.value = ''; messageInput.placeholder = 'Describe the situation, what you have tried, and what outcome you need.'; messageInput.focus();
  });
  sessionSelect.addEventListener('change', async () => {
    if (!sessionSelect.value) { activeSessionId = null; activeAttemptId = null; activeAttemptStatus = null; conversation.replaceChildren(); debriefButton.hidden = true; repeatButton.hidden = true; debriefPanel.hidden = true; difficultySelect.disabled = false; return; }
    try { await loadSession(sessionSelect.value); }
    catch (error) { addMessage('model', `Could not load this session: ${error.message}`); }
  });
  scenarioSelect.addEventListener('change', () => {
    if (activeSessionId) {
      activeSessionId = null; activeAttemptId = null; activeAttemptStatus = null; sessionSelect.value = '';
      conversation.replaceChildren(); debriefPanel.hidden = true; debriefPanel.replaceChildren();
      debriefButton.hidden = true; repeatButton.hidden = true; difficultySelect.disabled = false;
    }
    parentAttemptId = null;
    updateScenarioDescription();
    if (scenarioSelect.value && modeSelect.value === 'coach') modeSelect.value = 'roleplay';
  });
  difficultySelect.addEventListener('change', updateScenarioDescription);

  initQuiz();
  updateScenarioDescription();
  if (parentAttemptId) addMessage('model', 'Repeat practice is ready. Use the same difficulty to compare attempts more meaningfully.');
  if (sessionSelect.value) loadSession(sessionSelect.value).catch(error => addMessage('model', error.message));
})();
