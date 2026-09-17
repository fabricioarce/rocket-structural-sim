const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const output = path.resolve(process.argv[2] || path.join(__dirname, 'outputs'));
const source = fs.readFileSync(path.join(output, 'index.html'), 'utf8');
assert(!source.includes('@@'), 'Hay marcadores sin sustituir');
for (const match of source.matchAll(/(?:src|href)="([^"]+)"/g)) {
  const link = match[1];
  if (!link.startsWith('#') && !link.startsWith('https://')) {
    assert(fs.existsSync(path.join(output, link)), `Falta recurso: ${link}`);
  }
}
const payload = source.match(/<script id="study-data" type="application\/json">([\s\S]*?)<\/script>/)[1];
const scripts = [...source.matchAll(/<script>([\s\S]*?)<\/script>/g)];
const results = JSON.parse(fs.readFileSync(path.join(output, 'results.json'), 'utf8'));
const data = JSON.parse(payload);
assert.equal(data.cases.length, results.cases.length);
class Element {
  constructor(id = '') { this.id = id; this.value = ''; this.textContent = ''; this.innerHTML = ''; this.children = []; this.handlers = {}; }
  appendChild(child) { this.children.push(child); if (this.id === 'case-select' && !this.value) this.value = child.value; }
  replaceChildren() { this.children = []; }
  addEventListener(event, callback) { this.handlers[event] = callback; }
}
const elements = new Map([...source.matchAll(/id="([^"]+)"/g)].map(m => [m[1], new Element(m[1])]));
elements.get('study-data').textContent = payload;
elements.get('payload-limit').value = '0';
elements.get('metric-select').value = 'altitude_agl_m';
const context = vm.createContext({document: {getElementById: id => elements.get(id), createElement: () => new Element()}, console});
for (const script of scripts) vm.runInContext(script[1], context, {timeout: 5000});
assert.equal(elements.get('design-table').children.length, results.ranked_designs.length);
assert(elements.get('case-plot').innerHTML.includes('<svg'));
if (results.best_sampled_design) assert(elements.get('best').textContent.startsWith('Mejor caso'));
else assert(elements.get('best').textContent.startsWith('Ninguno'));
elements.get('flutter-limit').value = '1000';
elements.get('flutter-limit').handlers.input();
assert(elements.get('best').textContent.startsWith('Ninguno'));
elements.get('flutter-limit').value = String(data.limits.flutter_ratio);
elements.get('payload-limit').value = '1000';
elements.get('payload-limit').handlers.input();
assert(elements.get('best').textContent.startsWith('Ninguno'));
elements.get('flutter-limit').value = '-1';
elements.get('flutter-limit').handlers.input();
assert(elements.get('best').textContent.startsWith('Introduce'));
for (const row of data.cases) {
  for (const metric of ['altitude_agl_m', 'airspeed_m_s', 'flutter_speed_m_s', 'flutter_ratio']) {
    elements.get('case-select').value = row.case_id;
    elements.get('metric-select').value = metric;
    elements.get('case-select').handlers.change();
    const svg = elements.get('case-plot').innerHTML;
    assert(svg.includes('<path'));
    assert(!svg.includes('NaN') && !svg.includes('Infinity'));
  }
}
console.log(`OK: recursos locales, JSON, tabla, filtros sin candidatos y ${data.cases.length*4} curvas del inspector. Prueba de lógica DOM, no de renderizado de navegador.`);
