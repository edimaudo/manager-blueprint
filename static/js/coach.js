(() => {
  const quizBox = document.getElementById('coach-quiz');
  const recommendation = document.getElementById('coach-recommendation');
  const form = document.getElementById('coach-form');
  const conversation = document.getElementById('conversation');
  const messageInput = document.getElementById('message');
  const modeSelect = document.getElementById('mode');
  const capabilitySelect = document.getElementById('capability');
  const scenarioSelect = document.getElementById('scenario');
  const sessionSelect = document.getElementById('saved-sessions');
  const debriefButton = document.getElementById('debrief');
  const newSessionButton = document.getElementById('new-session');
  if (!quizBox || !form) return;

  let activeSessionId = null;
  let isBusy = false;
  const scenarioMap = {};
  [...scenarioSelect.options].forEach(option => { if (option.value) scenarioMap[option.value] = option.textContent; });

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

  async function parseResponse(response) {
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || 'The request could not be completed.');
    return data;
  }

  async function refreshSessions() {
    const data = await parseResponse(await fetch('/api/coach/sessions'));
    const selected = activeSessionId;
    sessionSelect.innerHTML = '<option value="">New session</option>';
    data.sessions.forEach(session => {
      const option = document.createElement('option');
      option.value = session.id;
      option.textContent = `${session.title} · ${String(session.updated_at || '').slice(0, 10)}`;
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
    conversation.replaceChildren();
    data.messages.forEach(item => addMessage(item.role, item.content));
    debriefButton.hidden = !(data.session.scenario_slug && data.session.mode === 'roleplay');
    updateScenarioDescription();
  }

  function updateScenarioDescription() {
    const selected = scenarioSelect.value;
    const optionText = selected ? scenarioMap[selected] : '';
    const node = document.getElementById('scenario-description');
    node.textContent = optionText
      ? `${optionText}. The coach will play the counterpart in the scenario. Use “Debrief practice” when you are ready to review your approach.`
      : 'Choose a scenario to practise a realistic management situation with your coach.';
    if (selected) {
      const selectedOption = scenarioSelect.selectedOptions[0];
      const selectedCapability = selectedOption?.dataset.capability;
      if (selectedCapability) capabilitySelect.value = selectedCapability;
      if (modeSelect.value === 'coach') modeSelect.value = 'roleplay';
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
          session_id: activeSessionId
        })
      }));
      activeSessionId = data.session_id;
      addMessage('model', data.answer);
      await refreshSessions();
      debriefButton.hidden = !(scenarioSelect.value && mode === 'roleplay');
      if (mode === 'feedback') debriefButton.hidden = true;
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
          const title = document.createElement('h3'); title.textContent = result.recommended_coach;
          const reason = document.createElement('p'); reason.textContent = result.reasoning;
          const approach = document.createElement('p'); approach.textContent = result.approach;
          recommendation.append(title, reason, approach);
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
  debriefButton.addEventListener('click', () => sendMessage('Pause the role-play and debrief how I handled the conversation so far. Identify what worked, what I should improve, and a stronger alternative response.', 'feedback'));
  newSessionButton.addEventListener('click', () => {
    activeSessionId = null; sessionSelect.value = ''; conversation.replaceChildren(); debriefButton.hidden = true; messageInput.value = ''; messageInput.focus();
  });
  sessionSelect.addEventListener('change', async () => {
    if (!sessionSelect.value) { activeSessionId = null; conversation.replaceChildren(); debriefButton.hidden = true; return; }
    try { await loadSession(sessionSelect.value); }
    catch (error) { addMessage('model', `Could not load this session: ${error.message}`); }
  });
  scenarioSelect.addEventListener('change', updateScenarioDescription);

  initQuiz();
  updateScenarioDescription();
  if (sessionSelect.value) loadSession(sessionSelect.value).catch(error => addMessage('model', error.message));
})();
