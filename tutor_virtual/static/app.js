const form = document.querySelector('#ask-form');
const input = document.querySelector('#message');
const level = document.querySelector('#level');
const conversation = document.querySelector('#conversation');
const welcome = document.querySelector('#welcome');
const feedback = document.querySelector('#feedback');
const send = document.querySelector('#send');
const reset = document.querySelector('#reset');
let mode = 'explicar';
let history = [];
let busy = false;

function counter() { document.querySelector('#counter').textContent = `${input.value.length.toLocaleString('es-MX')} / 4,000`; }
function setBusy(value) {
  busy = value;
  send.disabled = value;
  reset.disabled = value;
  level.disabled = value;
  input.disabled = value;
  document.querySelectorAll('[data-mode], [data-example]').forEach(button => { button.disabled = value; });
}
function addMessage(role, text) {
  welcome.hidden = true;
  const article = document.createElement('article');
  article.className = `message ${role}`;
  const label = document.createElement('h4');
  label.textContent = role === 'user' ? 'Tu pregunta' : 'Aula IA · Tutor';
  const body = document.createElement('p');
  body.textContent = text;
  article.append(label, body);
  conversation.append(article);
  conversation.scrollTop = conversation.scrollHeight;
}
document.querySelectorAll('[data-mode]').forEach(button => {
  button.addEventListener('click', () => {
    mode = button.dataset.mode;
    document.querySelectorAll('[data-mode]').forEach(item => {
      item.classList.toggle('active', item === button);
      item.setAttribute('aria-pressed', String(item === button));
    });
    input.focus();
  });
});
document.querySelectorAll('[data-example]').forEach(button => {
  button.addEventListener('click', () => { input.value = button.dataset.example; counter(); input.focus(); });
});
input.addEventListener('input', counter);
reset.addEventListener('click', () => {
  history = [];
  conversation.querySelectorAll('.message').forEach(item => item.remove());
  welcome.hidden = false;
  feedback.textContent = '';
  feedback.classList.remove('error');
  input.value = '';
  counter();
  input.focus();
});
form.addEventListener('submit', async event => {
  event.preventDefault();
  if (busy || !input.value.trim()) return;
  const message = input.value.trim();
  setBusy(true);
  feedback.classList.remove('error');
  feedback.textContent = 'El tutor está preparando tu respuesta…';
  try {
    const response = await fetch('/api/ask', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message, mode, level: level.value, history}),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'No se pudo obtener la respuesta.');
    addMessage('user', message);
    addMessage('assistant', data.answer);
    history.push({role: 'user', content: message}, {role: 'assistant', content: data.answer});
    history = history.slice(-8);
    input.value = '';
    counter();
    feedback.textContent = 'Puedes continuar con una pregunta o cambiar de modo.';
  } catch (error) {
    feedback.classList.add('error');
    feedback.textContent = error instanceof TypeError ? 'No se pudo conectar con el tutor. Comprueba que la aplicación siga abierta.' : error.message;
  } finally { setBusy(false); input.focus(); }
});
