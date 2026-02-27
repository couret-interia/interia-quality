
/* --- Tool box & beautify init --- */

const _TOOLHTML = `

<div class="container" id="tools">
<input class="tool toggler" type="checkbox" id="toggler_iiatools">
<label for="toggler_iiatools"><h4>🧰 Tools</h4></label>
<div class="grid">

<!-- https://github.com/josdejong/jsoneditor -->
<div class="tool" id="json">
    <input class="toggler custom" type="checkbox" id="toggler_jedit" checked="">
    <label class="custom" for="toggler_jedit"><h3>🔑 JSON Tool</h3> <span title="Hide">🔼</span><span title="Show">🔽</span></label>
    <div class="card" id="card-2">
        <a href="javascript:void(0);" class="tfs" data-id="jsoneditor" title="FullScreen" onclick="document.getElementById('tog_jedit-1').checked = true;">⛶</a>
        <div id="settingsjedit" class="header-line">
            <h2 title="JSON Editor">JSON</h2>
            <span class="badge">

                 · <input type="file" accept=".json" id="loadDocumentjedit" value="Load"><label for="loadDocumentjedit" title="Load a JSON document"> 💻 Load </label>
                 · <input type="button"              id="saveDocumentjedit" value="Save"><label for="saveDocumentjedit" title="Save a JSON document"> 💾 Save </label>

            </span>
        </div>
        <input class="toggler custom" type="checkbox" id="tog_jedit-1" checked="">
        <label class="custom" for="tog_jedit-1"><h3 class="no-sticky">JSON Editor</h3> <span title="Hide">🔼</span><span title="Show">🔽</span></label>

        <div id="jsoneditor"></div>

    </div>
</div>

<!-- http://incaseofstairs.com/jsdiff/ | github.com/kpdecker/jsdiff -->
<div class="tool" id="diff">
    <input class="toggler custom" type="checkbox" id="toggler_diff" checked="">
    <label class="custom" for="toggler_diff"><h3>🎯 Diff Tool</h3> <span title="Hide Diff">🔼</span><span title="Show Diff">🔽</span></label>
    <div class="card" id="card-1">
        <a href="javascript:void(0);" class="tfs" data-id="card-1" title="FullScreen">⛶</a>
        <div id="settings" class="header-line">
            <h2 title="Diff">Diff</h2>
            <span class="badge"> ·
                <input id="dfc" type="radio" name="diff_type" value="diffChars"><label for="dfc" title="Chars">🔤</label>
                <input id="dfw" type="radio" name="diff_type" value="diffWords"><label for="dfw" title="Words">📜</label>
                <input id="dfl" type="radio" name="diff_type" value="diffLines" checked=""><label for="dfl" title="Lines">📄</label>
                <input id="dfp" type="radio" name="diff_type" value="diffPatch"><label for="dfp" title="Patch">🧩</label>
                · <input id="dfa" type="checkbox" name="diff_area">             <label for="dfa" title="Areas">🔍</label>
            </span>
        </div>
        <div id="c" class="grid hide">
            <div id="diff_a" class="card"><h4>🔧 Old Snippet (Diff A) <a href="javascript:void(0);" id="dfs_a" class="tfs" data-id="diff_a" title="FullScreen">⛶ </a></h4><textarea id="a"></textarea><a href="javascript:void(0);" id="tfs_a" class="tfs" data-id="a" title="FullScreen">⛶ </a></div>
            <div id="diff_b" class="card"><h4>🔧 New Snippet (Diff B) <a href="javascript:void(0);" id="dfs_b" class="tfs" data-id="diff_b" title="FullScreen">⛶ </a></h4><textarea id="b"></textarea><a href="javascript:void(0);" id="tfs_b" class="tfs" data-id="b" title="FullScreen">⛶ </a></div>
        </div>
        <input class="toggler custom" type="checkbox" id="tog_diff-1" checked="">
        <label class="custom" for="tog_diff-1"><h3>Diff Snippet</h3> <span title="Hide">🔼</span><span title="Show">🔽</span></label>
        <pre class="iiasrc" id="result" data-id="-1" data-ln-start-from="0">  </pre>
    </div>
</div></div></div>
`;

// Inject toolbox html
document.querySelector('#content').insertAdjacentHTML('afterend', _TOOLHTML);
console.log("🎨 Inject toolbox html");
/* --- Init hljs link (css) & script tag --- */

const HLJS_DEF = 'cybertopia-dimmer', // ir-black paraiso-dark
  HLJSLNG = [
    'plaintext',
    'python',
    'markdown',
    'latex'
  ],
  HLJS_U = 'https://cdn.jsdelivr.net/gh/highlightjs/cdn-release@latest/build/';

// Inject hljs default theme
let h = HLJS_U + 'styles/' + HLJS_DEF + '.min.css';
// document.write('<link id="hljsheadlink" href="' + h.replace('/', '\/') + '" rel="stylesheet">');
addCssLinkInHead(h, 'beforeend', 'hljsheadlink');

// Inject hljs js
// core
h = HLJS_U + 'highlight.min.js';
addJsInDom(h, 'afterbegin', true, true, '', function(){ // (src, pos, defer, head, type, cb)
  console.log("🎨 highlightjs loaded!");

  // load default languages
  for (let i = 0; i < HLJSLNG.length; i++) {
    _hljsLangJsInDom(HLJSLNG[i]);
  }

  if ('object' == typeof hljs) {
    hljs.configure({
      cssSelector: 'pre'
      // … other options aren't changed
      // languages: ['python','latex','markdown'],
      // noHighlightRe: /^do-not-highlightme$/i,
      // languageDetectRe: /\bgrammar-([\w-]+)\b/i, // for `grammar-swift` style CSS naming
      // classPrefix: ''     // don't append class prefix
    });
    let h = 'https://cdn.jsdelivr.net/npm/highlightjs-line-numbers.js@2.9.0/dist/highlightjs-line-numbers.min.js';
    // document.write('<script src="' + h.replace('/', '\/') + '"><\/script>');
    addJsInDom(h, ' ', !1, !1, '', function(){
      console.log("🎨 highlightjs line-numbers loaded!"); // 🯰🯱🯲🯳🯴🯵🯶🯷🯸🯹
    });
    console.log("🧩 highlightjs line-numbers on load");
  }
});
console.log("🧩 highlightjs on load");

const _HLJS_LANGS_LOADED = [];
function _hljsLangJsInDom(lang) {
  // lang in _HLJS_LANGS_LOADED
  if (_HLJS_LANGS_LOADED.indexOf(lang) > -1) {
    return true;
  }
  _HLJS_LANGS_LOADED.push(lang);
  h = HLJS_U + 'languages/' + lang + '.min.js';
  // document.write('<script src="' + h.replace('/', '\/') + '"><\/script>');
  addJsInDom(h);
  console.log("🧩 highlightjs lang on load: " + lang);
}

// hljs 11.11 : https://duckduckgo.com/?t=lm&q=document.createElement(%27select%27)%3B+option+by+array&ia=web&iax=qa
const HLJS_THEMES = [
  '1c-light',
  'a11y-dark',
  'a11y-light',
  'agate',
  'androidstudio',
  'an-old-hope',
  'arduino-light',
  'arta',
  'ascetic',
  'atom-one-dark',
  'atom-one-dark-reasonable',
  'atom-one-light',
  'brown-paper',
  'codepen-embed',
  'color-brewer',
  'cybertopia-cherry',
  'cybertopia-dimmer',
  'cybertopia-icecap',
  'cybertopia-saturated',
  'dark',
  'default',
  'devibeans',
  'docco',
  'far',
  'felipec',
  'foundation',
  'github',
  'github-dark',
  'github-dark-dimmed',
  'gml',
  'googlecode',
  'gradient-dark',
  'gradient-light',
  'grayscale',
  'hybrid',
  'idea',
  'intellij-light',
  'ir-black',
  'isbl-editor-dark',
  'isbl-editor-light',
  'kimbie-dark',
  'kimbie-light',
  'lightfair',
  'lioshi',
  'magula',
  'mono-blue',
  'monokai',
  'monokai-sublime',
  'night-owl',
  'nnfx-dark',
  'nnfx-light',
  'nord',
  'obsidian',
  'panda-syntax-dark',
  'panda-syntax-light',
  'paraiso-dark',
  'paraiso-light',
  'pojoaque',
  'purebasic',
  'qtcreator-dark',
  'qtcreator-light',
  'rainbow',
  'rose-pine',
  'rose-pine-dawn',
  'rose-pine-moon',
  'routeros',
  'school-book',
  'shades-of-purple',
  'srcery',
  'stackoverflow-dark',
  'stackoverflow-light',
  'sunburst',
  'tokyo-night-dark',
  'tokyo-night-light',
  'tomorrow-night-blue',
  'tomorrow-night-bright',
  'vs',
  'vs2015',
  'vs-dark',
  'xcode',
  'xt256',
]; // 11.11

// base16/ (oldies?)
const HLJS_THEMES_BASE = [
  '3024',
  'apathy',
  'apprentice',
  'ashes',
  'atelier-cave',
  'atelier-cave-light',
  'atelier-dune',
  'atelier-dune-light',
  'atelier-estuary',
  'atelier-estuary-light',
  'atelier-forest',
  'atelier-forest-light',
  'atelier-heath',
  'atelier-heath-light',
  'atelier-lakeside',
  'atelier-lakeside-light',
  'atelier-plateau',
  'atelier-plateau-light',
  'atelier-savanna',
  'atelier-savanna-light',
  'atelier-seaside',
  'atelier-seaside-light',
  'atelier-sulphurpool',
  'atelier-sulphurpool-light',
  'atlas',
  'bespin',
  'black-metal',
  'black-metal-bathory',
  'black-metal-burzum',
  'black-metal-dark-funeral',
  'black-metal-gorgoroth',
  'black-metal-immortal',
  'black-metal-khold',
  'black-metal-marduk',
  'black-metal-mayhem',
  'black-metal-nile',
  'black-metal-venom',
  'brewer',
  'bright',
  'brogrammer',
  'brush-trees',
  'brush-trees-dark',
  'chalk',
  'circus',
  'classic-dark',
  'classic-light',
  'codeschool',
  'colors',
  'cupcake',
  'cupertino',
  'danqing',
  'darcula',
  'darkmoss',
  'darktooth',
  'dark-violet',
  'decaf',
  'default-dark',
  'default-light',
  'dirtysea',
  'dracula',
  'edge-dark',
  'edge-light',
  'eighties',
  'embers',
  'equilibrium-dark',
  'equilibrium-gray-dark',
  'equilibrium-gray-light',
  'equilibrium-light',
  'espresso',
  'eva',
  'eva-dim',
  'flat',
  'framer',
  'fruit-soda',
  'gigavolt',
  'github',
  'google-dark',
  'google-light',
  'grayscale-dark',
  'grayscale-light',
  'green-screen',
  'gruvbox-dark-hard',
  'gruvbox-dark-medium',
  'gruvbox-dark-pale',
  'gruvbox-dark-soft',
  'gruvbox-light-hard',
  'gruvbox-light-medium',
  'gruvbox-light-soft',
  'hardcore',
  'harmonic16-dark',
  'harmonic16-light',
  'heetch-dark',
  'heetch-light',
  'helios',
  'hopscotch',
  'horizon-dark',
  'horizon-light',
  'humanoid-dark',
  'humanoid-light',
  'ia-dark',
  'ia-light',
  'icy-dark',
  'ir-black',
  'isotope',
  'kimber',
  'london-tube',
  'macintosh',
  'marrakesh',
  'materia',
  'material',
  'material-darker',
  'material-lighter',
  'material-palenight',
  'material-vivid',
  'mellow-purple',
  'mexico-light',
  'mocha',
  'monokai',
  'nebula',
  'nord',
  'nova',
  'ocean',
  'oceanicnext',
  'onedark',
  'one-light',
  'outrun-dark',
  'papercolor-dark',
  'papercolor-light',
  'paraiso',
  'pasque',
  'phd',
  'pico',
  'pop',
  'porple',
  'qualia',
  'railscasts',
  'rebecca',
  'ros-pine',
  'ros-pine-dawn',
  'ros-pine-moon',
  'sagelight',
  'sandcastle',
  'seti-ui',
  'shapeshifter',
  'silk-dark',
  'silk-light',
  'snazzy',
  'solar-flare',
  'solar-flare-light',
  'solarized-dark',
  'solarized-light',
  'spacemacs',
  'summercamp',
  'summerfruit-dark',
  'summerfruit-light',
  'synth-midnight-terminal-dark',
  'synth-midnight-terminal-light',
  'tango',
  'tender',
  'tomorrow',
  'tomorrow-night',
  'twilight',
  'unikitty-dark',
  'unikitty-light',
  'vulcan',
  'windows-10',
  'windows-10-light',
  'windows-95',
  'windows-95-light',
  'windows-high-contrast',
  'windows-high-contrast-light',
  'windows-nt',
  'windows-nt-light',
  'woodland',
  'xcode-dusk',
  'zenburn'
]; // base16/

// Init hjjs themes 4 opt tog, link.href & _LS
const HLJS_TITLES = ['Classics', 'Base16 (oldies)'];

function hjjsTogThemesInit() {
  let s = document.createElement('select'),
    o = document.createElement('option'),
    p = document.createElement('optgroup');
  const HLJS_GRP = [HLJS_THEMES, HLJS_THEMES_BASE], // BASE base16/
    u  = HLJS_U + 'styles/',
    l  = document.getElementById('hljsheadlink'),
    tb = document.querySelector('.light-switch.top-bar.top-bar-right');
  s.id        = 'hljstog';
  s.name      = 'hljsthemestoggle';
  s.title     ='💠 Choose to memorize hljs theme';
  s.className = "iia-hljs-top-bar-menu"
  for (let x = 0; x < HLJS_GRP.length; x++) {
    let g = p.cloneNode(true);
    g.label = '🎨 ' + HLJS_TITLES[x];
    for (let i = 0; i < HLJS_GRP[x].length; i++) {
      let t = o.cloneNode(true);
      t.textContent = HLJS_GRP[x][i];
      t.value = HLJS_GRP[x][i];
      if(HLJS_GRP[x][i] == HLJS_DEF) {
        t.selected = true;
      }
      g.appendChild(t)
    }
    s.appendChild(g);
  }
  // beforebegin, beforeend, afterend
  const position = "afterbegin";
  tb.insertAdjacentElement(position, s);
  s = document.getElementById('hljstog');
  s.addEventListener('change', function (e) {
    let sixteen = '',
      chk = document.querySelector('#' + e.target.id + ' option:checked');
    // parentElement: optgroup '🎨 Classics' != chk
    if (chk && chk.parentElement && !(chk.parentElement.label.search(/lassics/) > -1)) {
      sixteen = 'base16/';
    }
    l.href = u + sixteen + e.target.value + '.min.css'; // up link tag href
    if (chk && _LS) {
      if(e.target.value != HLJS_DEF) {
        window.localStorage.setItem('iia-hljs', sixteen + e.target.value);
      }else{
        window.localStorage.removeItem('iia-hljs');
      }
    }
  });
  // Set hljf theme from localStorage & change it
  if (_LS && window.localStorage.getItem('iia-hljs')) {
    let k = window.localStorage.getItem('iia-hljs');
    // Check preview selected opt exist
    const sopt = Array.from(s.options).find(item => item.text === k.replace('base16/', ''));
    if(sopt && sopt.value) {
      s.value = sopt.value;
      /* Trigger the onchange event element when the page loads */
      // Create a new event
      const event = new Event('change', {
        bubbles: true,
        cancelable: true
      });
      // Dispatch the event
      s.dispatchEvent(event);
    }else{
      window.localStorage.removeItem('iia-hljs');
    }
  }
}

// https://stackoverflow.com/a/78522501 ::: https://stackoverflow.com/questions/78520720/how-to-remove-multiple-dom-elements-using-a-single-function-in-javascript#78522501
function remove(removable) {
  if (!removable) return;
  if ("length" in removable) {
    for (const element of Array.from(removable)) element.remove();
  } else removable.remove();
}

// Get txt from hljs+ln
function goodCode(preElement) {
  if (!preElement) return '';
  const p = preElement.cloneNode(true),
    lns   = p.querySelectorAll('.hljs-ln-line.hljs-ln-code');
  if(lns.length > 0) {
    // + tweak 2 fix hljs(ln): add one space on empty line (not in source code)
    const itemTexts = [...lns].map(item => item.textContent.replace(/\s$/, ''));
    return itemTexts.join("\n") + "\n";
  }
  return p.textContent; // innerText
}

function createCopyButton(preElement) {
  const button = document.createElement('button');
  button.id = 'copy_' + preElement.id + '';
  button.textContent = '🌈 Copy code';
  button.className = 'iiasrc copy-button';

  button.addEventListener('click', (e) => {
    const preElement = document.querySelector('#' + e.target.id.replace('copy_',''));
    const btn = e.target;
    navigator.clipboard.writeText(goodCode(preElement))
      .then(() => {
        showNotification(btn); // Show Copied (by default)
      })
      .catch(err => {
        console.error('⚠️ Copy fail: ', err);
        let btnstr = '⚠️ Copy fail!',
        str = '⚠️ Error when get code! See Error in console.',
        time = 10000;
        showNotification(btn, btnstr, str, time);
      });
  });

  // Inject button
  const position = "beforebegin";
  preElement.insertAdjacentElement(position, button);

  // Set language for hljs
  const aId  = preElement.id.split('_');

  // Only #(old|new)_snippet (not 4 #result)
  if (aId.length > 1) {
    const fId  = 'card' + aId[1].replace('snippet', ''),
      file = document.querySelector('#' + fId + ' h2');
    if (file) {
      // Set language for hljs
      preElement.classList.add('language-' + fileType(file.textContent));
    }
  }

  // Apply hilightJS [Here an example without the <code> tag.](http://stackoverflow.com/questions/10936854/ddg#10937327)
  hljs.highlightElement(preElement);
  hljs.lineNumbersBlock(preElement);
}

// Toggle card element without head
function toggleCardContents(el) {
  const chlds = el.children;
  for (let c = 0; c < chlds.length; c++) {
    if (chlds[c].classList.contains('header-line')) {
      // console.log('---toggleCardContents: ' + c, chlds[c]);
      const h2 = chlds[c].firstElementChild;
      h2.classList.toggle('closed');
      h2.title = '🔁 ' + (h2.title == '🔁 Show Snippets'?'Hide':'Show') + ' Snippets';
      continue;
    }
    if (chlds[c].classList.contains('tool')) {
      // close if Diff (but maybe not user frienly?)
      // if (chlds[c].firstElementChild.checked && chlds[c - 1].classList.contains('hide')) {
        // chlds[c].firstElementChild.checked = !true;
      // }
      continue;
    }
    chlds[c].classList.toggle('hide');
  }
}

// Where el is the DOM element you'd like to test for visibility (http://stackoverflow.com/questions/19669786/ddg#21696585)
function isHidden(el) {
  return (el.offsetParent === null)
}
// On the other hand, if you do have position fixed elements that might get caught in this search, you will sadly (and slowly) have to use window.getComputedStyle(). The function in that case might be:
// Where el is the DOM element you'd like to test for visibility (renamed)
function isHiddenComputed(el) {
    var style = window.getComputedStyle(el);
    return (style.display === 'none')
}

function initsticky() {
  const preElements = document.querySelectorAll('pre.iiasrc'),
    buttons         = document.querySelectorAll('button.iiasrc'),            // best with : more user fiendly : on ends, button removed too late (chevauchement de 2 boutons) (css rule?)
    h3s             = document.querySelectorAll('.card h3:not(.no-sticky)'), // old or new snippet
    h2s             = document.querySelectorAll('.card div.header-line'),    // h2 + badge // title of item (card) : id="head_snippet${idx}"
    atop            = 0,
    otop            = 72,
    lastModJson     = window.lastMod || ''; // ai_response.json
  window.onscroll = function() {
    for (let i = 0; i < preElements.length; ++i) {
      if(preElements[i].id) {
        const s = (
          preElements[i].getBoundingClientRect().top < (atop + otop - 20)
          && preElements[i].getBoundingClientRect().bottom > (atop + otop + 120) // 150
        );
        if (s) {
          buttons[i].classList.add('sticky');
          h3s[i].classList.add('sticky');
        } else {
          buttons[i].classList.remove('sticky');
          h3s[i].classList.remove('sticky');
        }
        if( i % 2) continue; // idea 2 fix one time
        let z = parseInt(preElements[i].getAttribute('data-id'));
        if (Number.isNaN(z)) continue;   // fix 4 diff
        if (z == -1) z = h2s.length - 1; // fix 4 diff (todo: 4 other?)
        let c = h2s[z].parentElement;    // Add .parentElement if h2 only
        let h = c.getBoundingClientRect().top + c.getBoundingClientRect().height;
        // Note c.getBoundingClientRect().bottom === (c.getBoundingClientRect().top + c.getBoundingClientRect().height)
        let t = (
          c.getBoundingClientRect().top < atop &&
          c.getBoundingClientRect().bottom > (atop + 150) // (window.screenTop + otop)
        );
        if (t) {
          h2s[z].classList.add('sticky');
        } else {
          h2s[z].classList.remove('sticky');
        }
      }
    }
  }

  // Init Hide/Show tweak
  const memOk = (_LS && lastModJson);
  // Snippets
  for (let i = 0; i < h3s.length; ++i) {
    h3s[i].addEventListener('click', function (e) {
      // Get real Snip name on Hide/Show (fix when sticky)
      window.scrollTo({
        top: window.scrollY + 1
      });
      window.scrollTo({
        top: window.scrollY - 1
      });
      if (memOk) {
        const togId = e.target.parentElement.getAttribute('for');
        if (document.getElementById(togId).checked) {
          localStorage.setItem(togId, lastModJson); // go to 🗹
        } else {
          localStorage.removeItem(togId); // go to 🗸
        }
      }
    });
    // Snip Open?
    if (memOk) {
      const togId = h3s[i].parentElement.getAttribute('for');
      if (localStorage.getItem(togId) == lastModJson) {
        document.getElementById(togId).checked = false; // go to 🗹
      } else {
        localStorage.removeItem(togId); // reset (old)
      }
    }
  }
  // Cards (not for tool card)
  for (let i = 0; i < h2s.length; ++i) {
    const cardId = h2s[i].parentElement.id; // Card id
    const nr = parseInt(cardId.replace('card', '')) + 1;
    if (nr < 1) continue; // not for tool
    h2s[i].parentElement.classList.add(str2className(h2s[i].firstElementChild.textContent));
    h2s[i].firstElementChild.addEventListener('click', function (e) {
      // Get real Snip name on Hide/Show (fix when sticky)
      window.scrollTo({
        top: window.scrollY + 1
      });
      window.scrollTo({
        top: window.scrollY - 1
      });
      if (memOk) {
        const card = e.target.parentElement.parentElement; // Card
        const cardId = card.id;
        toggleCardContents(card);
        if (isHidden(card.lastElementChild)) {
          localStorage.setItem(cardId, lastModJson); // go to 🗹
        } else {
          localStorage.removeItem(cardId); // go to 🗸
        }
      }
    });
    h2s[i].firstElementChild.title = '🔁 Hide Snippets';

    const cardnr = document.createElement('span');
    cardnr.id = 'num_' + cardId + '';

    cardnr.textContent = nr;
    cardnr.title = nr;
    cardnr.className = 'num_snip';
    // Inject cardnr in badge
    const position = "afterbegin";
    h2s[i].firstElementChild.nextElementSibling.insertAdjacentElement(position, cardnr);

    // card Open?
    if (memOk) {
      if (localStorage.getItem(cardId) == lastModJson) {
        // hide
        toggleCardContents(h2s[i].parentElement);
      } else {
        localStorage.removeItem(cardId); // reset (it's old)
      }
    }
  }
}

// http://stackoverflow.com/questions/14226803/ddg#47480429
const delay = ms => new Promise(res => setTimeout(res, ms));
function stylePreElements() {
  const preElements = document.querySelectorAll('pre.iiasrc');
  if (preElements) {
    console.log("🧩 Check hljs & hljs.lineNumbersBlock");
    if ('undefined' != typeof hljs && 'undefined' != typeof hljs.lineNumbersBlock) {
      console.log("💫 Start HighLight");
      preElements.forEach(pre => {
        if (pre.id) {
          createCopyButton(pre);
        }
      });
      initsticky();
      hjjsTogThemesInit();
      diffAddHeads();
      console.log("🌈 Beautified!");
      return 0;
    }
  }
  return 1;
}
window.init = async () => {
  await delay(200);
  console.log("Waited 200ms");
  if (stylePreElements()) {
    init();
  }
};


/* --- tiny fulscreen helper --- */

const tfs = document.querySelectorAll('.tfs');
for(let i = 0; i < tfs.length; ++i) {
  tfs[i].addEventListener('click', function(e){
    // if already full screen; exit else go fullscreen
    if (document.fullscreenElement) {
      document.exitFullscreen();
    } else {
      document.querySelector('#'+e.target.getAttribute('data-id'))?.requestFullscreen();
    }
  });
}

/* --- jsdiff --- */

addJsInDom('https://cdn.jsdelivr.net/npm/diff@8.0.2/dist/diff.min.js', 'afterbegin', true, true); // (h, 'beforeend', true, true);
console.log("🧩 jsdiff on load");

window.addEventListener('load', function () {
  const dfa = document.querySelector('#dfa'); // diff_area (Toggle Area's)
  dfa.addEventListener('click', function(e) {
    document.querySelector('#c').classList.toggle('hide');
    if(_LS) {
      if(e.target.checked) localStorage.setItem('dta', 'checked');
      else localStorage.removeItem('dta');
    }
  });

  if(_LS && localStorage.getItem('dta')) dfa.checked = true;
  else dfa.checked = false; // Fix F5 (Reload page)
  if(dfa.checked) document.querySelector('#c').classList.toggle('hide');;
  console.log("🎯 Diff: codes editor 🔍 " + (dfa.checked ? "Showed" : "Hide"));
});

// Load Diff codes
function diffSet(id) {
  const a = document.querySelector('#a'),                                // textarea a
    b = document.querySelector('#b'),                                    // textarea b
    o = document.querySelector('#' + id.replace('card', 'old_snippet')), // preElement
    n = document.querySelector('#' + id.replace('card', 'new_snippet')), // preElement
    u = o ? parseInt(o.getAttribute('data-ln-start-from')) : 1,          // 1st line old
    s = n ? parseInt(n.getAttribute('data-ln-start-from')) : 1,          // 1st line new
    e = document.querySelector('#' + id + ' h2')?.textContent;           // card h2 (Filename)
  // Get Codes (of pre)
  a.value = o ? goodCode(o) : '';
  b.value = n ? goodCode(n) : '';
  // Up Ace val fix when is .hide
  aceEditSetValue(aceEdit[0], a.value, u);
  aceEditSetValue(aceEdit[1], b.value, s);
  // Up diff
  changed(e || '.txt');
}

// Load Diff in Snip Card
function diffMoveTo(id) {
  // set Codes
  diffSet(id);
  // Select the element to move
  const elementToMove = document.querySelector('#diff');
  // Open Tools. Note: the `.firstChild` is text
  elementToMove.firstElementChild.checked = true;
  elementToMove.querySelector('#tog_diff-1').checked = true;
  // Select the new parent where you want to move the element
  const newParent = document.getElementById(id); // card* 'newParentId'
  // Move the element Using appendChild
  newParent.appendChild(elementToMove);
  // Scroll to the position
  scrollToMe(elementToMove.id);
}

// Add (Re)Load Diff in Snip h2 (init)
function diffAddHeads() {
  const h = document.querySelectorAll('.card div.header-line'); // h2 + badge // title of item (card) : id="head_snippet${idx}"
  for (var i = 0; i < (h.length - 1); ++i) { // tweak (not for Diff -1)
    if(h[i].parentElement.id && !h[i].parentElement.parentElement.classList.contains('tool')) {
      const l = document.createElement('a');
      l.href        = 'javascript:void(0);';
      l.title       = '· Move The 🎯 Diff here.\n· Load (or reload) snippets on decks from pre element.';
      l.textContent = '🔨 Load Diff'
      l.addEventListener('click', function() {
        diffMoveTo(this.parentElement.parentElement.id);
        aceModeAuto(this.parentElement.querySelector('h2').textContent);
        const btnstr = '🎯 Diff Loaded!',
        str = '🎯 Diff snippets loaded from pre element!';
        showNotification(this, btnstr, str);
      });
      h[i].insertAdjacentElement('beforeend',l); // afterend
    }
  }
}

// jsdiff init (inspired by demo http://incaseofstairs.com/jsdiff/)
const a = document.getElementById('a');
const b = document.getElementById('b');
const result = document.getElementById('result');
let diffFileName = '.txt';
function changed(fileName) {
  const file = fileName ? '/' + fileName : diffFileName;
  diffFileName = file;
  var fragment = document.createDocumentFragment();
  var diff;
  if (window.diffType === 'diffPatch') {
    // We contort the patch into a similar data structure to that returned by diffChars,
    // diffWords, etc so that the same rendering code below can work on both.
    var pastHunkHeader = false;
    diff = Diff.createTwoFilesPatch('a' + file, 'b' + file, a.value, b.value)
      .split('\n')
      .map(function(entry) {
        const result = {
          value: entry + '\n',
        };
        if (entry.startsWith('@@')) {
          result.chunkHeader = true;
          pastHunkHeader = true;
        } else if (pastHunkHeader) {
          if (entry.startsWith('-')) {
            result.removed = true;
          } else if (entry.startsWith('+')) {
            result.added = true;
          }
        }
        return result;
      });
  }
  else {
    diff = Diff[window.diffType](a.value, b.value);
  }

  for (var i=0; i < diff.length; i++) {

    if (diff[i].added && diff[i + 1] && diff[i + 1].removed) {
      var swap = diff[i];
      diff[i] = diff[i + 1];
      diff[i + 1] = swap;
    }

    var node;
    if (diff[i].removed) {
      node = document.createElement('del');
      node.appendChild(document.createTextNode(diff[i].value));
    } else if (diff[i].added) {
      node = document.createElement('ins');
      node.appendChild(document.createTextNode(diff[i].value));
    } else if (diff[i].chunkHeader) {
      node = document.createElement('span');
      node.setAttribute('class', 'chunk-header');
      node.appendChild(document.createTextNode(diff[i].value));
    } else {
      node = document.createTextNode(diff[i].value);
    }
    fragment.appendChild(node);
  }

  result.textContent = '';
  result.appendChild(fragment);
}
// diffChars diffWords diffLines diffPatch
window.addEventListener('load', function () {
  const ds = _LS ? localStorage.getItem('diff-setting') || 'diffLines' : 'diffLines';
  document.querySelector('#settings [name="diff_type"][value="'+ds+'"]').checked = true;
  console.log("🎯 Diff is set to mode: " + ds);
  onDiffTypeChange(document.querySelector('#settings [name="diff_type"]:checked'));
});

a.onpaste = a.onchange =
b.onpaste = b.onchange = changed;

if ('oninput' in a) {
  a.oninput = b.oninput = changed;
} else {
  a.onkeyup = b.onkeyup = changed;
}

function onDiffTypeChange(radio) {
  window.diffType = radio.value;
  // document.title = "Diff " + radio.value.slice(4);
}

var radio = document.getElementsByName('diff_type');
for (var i = 0; i < radio.length; i++) {
  radio[i].onchange = function(e) {
    onDiffTypeChange(e.target);
    changed();
    _LS && localStorage.setItem('diff-setting', e.target.value);
  }
}
// diffInit end


// <script src="https://cdn.jsdelivr.net/npm/ace-builds@1.36/src-min-noconflict/ace.js">< /script>
// document.write('<script src="' + h.replace('/', '\/') + '"><\/script>');
addJsInDom('https://cdn.jsdelivr.net/npm/ace-builds@1.36/src-min-noconflict/ace.js', true, true);

/* --- Ace --- */

console.log("🧩 Acejs init!");

const position = 'beforebegin',
  acePosition  = 'afterend',
  aceEdit      = [];

// js supportedModes var converted :view-source:https://ace.c9.io/build/demo/kitchen-sink/demo.js
const aceSupportedModes = {
  'ABAP': 'abap',
  'ABC': 'abc',
  'ActionScript': 'as',
  'ADA': 'ada|adb',
  'Alda': 'alda',
  'Apache_Conf': '^htaccess|^htgroups|^htpasswd|^conf|htaccess|htgroups|htpasswd',
  'Apex': 'apex|cls|trigger|tgr',
  'AQL': 'aql',
  'AsciiDoc': 'asciidoc|adoc',
  'ASL': 'dsl|asl|asl.json',
  'Assembly_ARM32': 's',
  'Assembly_x86': 'asm|a',
  'Astro': 'astro',
  'AutoHotKey': 'ahk',
  'BatchFile': 'bat|cmd',
  'Basic': 'bas|bak',
  'BibTeX': 'bib',
  'C_Cpp': 'cpp|c|cc|cxx|h|hh|hpp|ino',
  'C9Search': 'c9search_results',
  'Cirru': 'cirru|cr',
  'Clojure': 'clj|cljs',
  'Cobol': 'CBL|COB',
  'coffee': 'coffee|cf|cson|^Cakefile',
  'ColdFusion': 'cfm|cfc',
  'Crystal': 'cr',
  'CSharp': 'cs',
  'Csound_Document': 'csd',
  'Csound_Orchestra': 'orc',
  'Csound_Score': 'sco',
  'CSS': 'css',
  'Curly': 'curly',
  'Cuttlefish': 'conf',
  'D': 'd|di',
  'Dart': 'dart',
  'Diff': 'diff|patch',
  'Django': 'djt|html.djt|dj.html|djhtml',
  'Dockerfile': '^Dockerfile',
  'Dot': 'dot',
  'Drools': 'drl',
  'Edifact': 'edi',
  'Eiffel': 'e|ge',
  'EJS': 'ejs',
  'Elixir': 'ex|exs',
  'Elm': 'elm',
  'Erlang': 'erl|hrl',
  'Flix': 'flix',
  'Forth': 'frt|fs|ldr|fth|4th',
  'Fortran': 'f|f90',
  'FSharp': 'fsi|fs|ml|mli|fsx|fsscript',
  'FSL': 'fsl',
  'FTL': 'ftl',
  'Gcode': 'gcode',
  'Gherkin': 'feature',
  'Gitignore': '^.gitignore',
  'Glsl': 'glsl|frag|vert',
  'Gobstones': 'gbs',
  'golang': 'go',
  'GraphQLSchema': 'gql',
  'Groovy': 'groovy',
  'HAML': 'haml',
  'Handlebars': 'hbs|handlebars|tpl|mustache',
  'Haskell': 'hs',
  'Haskell_Cabal': 'cabal',
  'haXe': 'hx',
  'Hjson': 'hjson',
  'HTML': 'html|htm|xhtml|we|wpy',
  'HTML_Elixir': 'eex|html.eex',
  'HTML_Ruby': 'erb|rhtml|html.erb',
  'INI': 'ini|conf|cfg|prefs',
  'Io': 'io',
  'Ion': 'ion',
  'Jack': 'jack',
  'Jade': 'jade|pug',
  'Java': 'java',
  'JavaScript': 'js|jsm|cjs|mjs',
  'JEXL': 'jexl',
  'JSON': 'json',
  'JSON5': 'json5',
  'JSONiq': 'jq',
  'JSP': 'jsp',
  'JSSM': 'jssm|jssm_state',
  'JSX': 'jsx',
  'Julia': 'jl',
  'Kotlin': 'kt|kts',
  'LaTeX': 'tex|latex|ltx|bib',
  'Latte': 'latte',
  'LESS': 'less',
  'Liquid': 'liquid',
  'Lisp': 'lisp',
  'LiveScript': 'ls',
  'Log': 'log',
  'LogiQL': 'logic|lql',
  'Logtalk': 'lgt',
  'LSL': 'lsl',
  'Lua': 'lua',
  'LuaPage': 'lp',
  'Lucene': 'lucene',
  'Makefile': '^Makefile|^GNUmakefile|^makefile|^OCamlMakefile|make',
  'Markdown': 'md|markdown',
  'Mask': 'mask',
  'MATLAB': 'matlab',
  'Maze': 'mz',
  'MediaWiki': 'wiki|mediawiki',
  'MEL': 'mel',
  'MIPS': 's|asm',
  'MIXAL': 'mixal',
  'MUSHCode': 'mc|mush',
  'MySQL': 'mysql',
  'Nasal': 'nas',
  'Nginx': 'nginx|conf',
  'Nim': 'nim',
  'Nix': 'nix',
  'NSIS': 'nsi|nsh',
  'Nunjucks': 'nunjucks|nunjs|nj|njk',
  'ObjectiveC': 'm|mm',
  'OCaml': 'ml|mli',
  'Odin': 'odin',
  'PartiQL': 'partiql|pql',
  'Pascal': 'pas|p',
  'Perl': 'pl|pm',
  'pgSQL': 'pgsql',
  'PHP': 'php|inc|phtml|shtml|php3|php4|php5|phps|phpt|aw|ctp|module',
  'PHP_Laravel_blade': 'blade\.php',
  'Pig': 'pig',
  'PLSQL': 'plsql',
  'Powershell': 'ps1',
  'Praat': 'praat|praatscript|psc|proc',
  'Prisma': 'prisma',
  'Prolog': 'plg|prolog',
  'Properties': 'properties',
  'Protobuf': 'proto',
  'PRQL': 'prql',
  'Puppet': 'epp|pp',
  'Python': 'py',
  'QML': 'qml',
  'R': 'r',
  'Raku': 'raku|rakumod|rakutest|p6|pl6|pm6',
  'Razor': 'cshtml|asp',
  'RDoc': 'Rd',
  'Red': 'red|reds',
  'RHTML': 'Rhtml',
  'Robot': 'robot|resource',
  'RST': 'rst',
  'Ruby': 'rb|ru|gemspec|rake|^Guardfile|^Rakefile|^Gemfile',
  'Rust': 'rs',
  'SaC': 'sac',
  'SASS': 'sass',
  'SCAD': 'scad',
  'Scala': 'scala|sbt',
  'Scheme': 'scm|sm|rkt|oak|scheme',
  'Scrypt': 'scrypt',
  'SCSS': 'scss',
  'SH': 'sh|bash|^.bashrc',
  'SJS': 'sjs',
  'Slim': 'slim|skim',
  'Smarty': 'smarty|tpl',
  'Smithy': 'smithy',
  'snippets': 'snippets',
  'Soy_Template': 'soy',
  'Space': 'space',
  'SPARQL': 'rq',
  'SQL': 'sql',
  'SQLServer': 'sqlserver',
  'Stylus': 'styl|stylus',
  'SVG': 'svg',
  'Swift': 'swift',
  'Tcl': 'tcl',
  'Terraform': 'tf", "tfvars", "terragrunt',
  'Tex': 'tex',
  'Text': 'txt',
  'Textile': 'textile',
  'Toml': 'toml',
  'TSX': 'tsx',
  'Turtle': 'ttl',
  'Twig': 'twig|swig',
  'Typescript': 'ts|mts|cts|typescript|str',
  'Vala': 'vala',
  'VBScript': 'vbs|vb',
  'Velocity': 'vm',
  'Verilog': 'v|vh|sv|svh',
  'VHDL': 'vhd|vhdl',
  'Visualforce': 'vfp|component|page',
  'Vue': 'vue',
  'Wollok': 'wlk|wpgm|wtest',
  'XML': 'xml|rdf|rss|wsdl|xslt|atom|mathml|mml|xul|xbl|xaml',
  'XQuery': 'xq',
  'YAML': 'yaml|yml',
  'Zeek': 'zeek|bro',
  'Zig': 'zig'
};

// Return lang type of file ('project/file.py');
function fileType(file) {
  let lang = 'text';
  if(!!file) {
    // Search in aceSupportedModes
    for(let m in aceSupportedModes){
      const rext    = new RegExp('\\.(' + aceSupportedModes[m] + ')$', 'gi');
      const matches = file.match(rext);
      if(matches && matches.length) {
        const fileExt = matches[0]; // Why not, but for what? (todo in tool, ace, ...)
        console.log(`💠 File ${file} is: ${m} (${fileExt})`);
        lang = m.toLowerCase();
        break;
      }
    }
  }
  return lang;
}

// Automatic ace('s) set Mode by file ('ace/mode/*);
function aceModeAuto(file,aceEditor) {
  let mode = fileType(file);
  if(typeof(aceEditor) != 'undefined'){
    aceEditor.session.setMode('ace/mode/' + mode);// getSession().setMode('ace/mode/' + mode);
  } else {
    for(let e = 0; e < aceEdit.length; e++){
      aceEdit[e].session.setMode('ace/mode/' + mode);// getSession().setMode('ace/mode/' + mode);
    }
  }
}

  /* --- init ace editor on textareas --- */

function download(filename, text) {
  const el = document.createElement('a');
  el.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  el.setAttribute('download', filename);
  el.style.display = 'none';
  document.body.appendChild(el);
  el.click();
  document.body.removeChild(el);
}

window.addEventListener('load', function () {

  console.log("🎨 textArea's load Ace!");

  const ta = document.querySelectorAll('textarea');
  for(let i = 0; i < ta.length; i++) {

    // Download to snippet TEXT btn
    const btntxt = document.createElement('button');
    btntxt.id = 'dowd_text_ta_' + ta[i].id + '';
    btntxt.textContent = '💾 TEXT';
    btntxt.title = 'Download this code to snippet-' + ta[i].id + '.txt';
    btntxt.className = 'btn-tiny btn-txt';
    btntxt.addEventListener('click', function(e) {
      const cId = this.id.replace('dowd_text_ta_',''), // common ID's with textta (a|b)
        ta = document.querySelector('#' + cId),
        filename = 'snippet-' + cId;
      showNotification(this, this.textContent.replace('💾', '📂'), '💾' + this.title);
      download(filename + '.txt', ta.value);
    });
    // ta[i].insertAdjacentElement(position, btntxt);
    ta[i].insertAdjacentElement(acePosition, btntxt);

    // Download to snippet JSON btn
    const btnjsn = document.createElement('button');
    btnjsn.id = 'dowd_json_ta_' + ta[i].id + '';
    btnjsn.textContent = '💾 JSON';
    btnjsn.title = 'Download code to snippet-' + ta[i].id + '.json';
    btnjsn.className = 'btn-tiny btn-jsn';
    btnjsn.addEventListener('click', function(e) {
      const cId = this.id.replace('dowd_json_ta_',''), // common ID's with textta (a|b)
        ta = document.querySelector('#' + cId),
        filename = 'snippet-' + cId;
      showNotification(this, this.textContent.replace('💾', '📂'), '💾' + this.title);
      download(filename + '.json', `{"${filename}":${JSON.stringify(ta.value)}}`);
    });
    // ta[i].insertAdjacentElement(position, btnjsn);
    ta[i].insertAdjacentElement(acePosition, btnjsn);

    // Copy to snippet JSON btn
    const btncjs = document.createElement('button');
    btncjs.id = 'copy_json_ta_' + ta[i].id + '';
    btncjs.textContent = '🌈 Copy JSON';
    btncjs.title = 'Copy code in JSON snippet to clipboard';
    btncjs.className = 'btn-tiny btn-cjs';
    btncjs.addEventListener('click', function(e) {
      const cId = this.id.replace('copy_json_ta_',''), // common ID's with textta (a|b)
        ta = document.querySelector('#' + cId),
        filename = 'snippet-' + cId;
      navigator.clipboard.writeText(`{"${filename}":${JSON.stringify(ta.value)}}`)
        .then(() => {
          showNotification(this, null, this.title.replace('Copy', '✅ Copied ') + '!');
        })
        .catch(err => {console.error('⚠️ Copy fail: ', err);});
    });
    // ta[i].insertAdjacentElement(position, btncjs);
    ta[i].insertAdjacentElement(acePosition, btncjs);

    const btntta = document.createElement('button');
    btntta.id = 'tog_ta_' + ta[i].id + '';
    btntta.textContent = '🔁 Show Text Area';
    btntta.title = 'Click to Show Text Area';
    btntta.className = 'btn-tiny btn-tta';
    btntta.addEventListener('click', function(e) {
      const cId = this.id.replace('tog_ta_',''); // common ID's with textarea (a|b)
      this.textContent = '🔁 Show ' + (this.textContent == '🔁 Show Text Area'?'Ace Editor':'Text Area');
      this.title = 'Click to Show ' + (this.textContent == 'Text Area'?'Ace Editor':'Text Area');
      // ~ document.getElementById(cId).classList.toggle('hide');
      ta[i].classList.toggle('hide');
      document.getElementById('ace_' + cId).classList.toggle('hide');
      // Fullscreen toggle a²ace_a or b²ace_b
      document.getElementById('tfs_' + cId).setAttribute('data-id', (ta[i].classList.contains('hide') ? 'ace_' : '') + cId);
    });
    // ta[i].insertAdjacentElement(position, btntta);
    ta[i].insertAdjacentElement(acePosition, btntta);

    // Add Ace
    const da = document.createElement('div');
    da.id = 'ace_' + ta[i].id + '';
    // da.textContent = 'Code';
    da.className = 'iia-ace';
    // Inject Ace
    // ta[i].insertAdjacentElement(position, da);
    ta[i].insertAdjacentElement(acePosition, da);

    aceEdit[i] = ace.edit('ace_' + ta[i].id);
    aceEdit[i].setTheme("ace/theme/twilight"); // todo: (auto ?) selector
    aceEdit[i].session.setMode('ace/mode/text');
    aceEdit[i].session.on('change', function () { // e,o
      ta[i].value = aceEdit[i].session.getValue(); // aceEdit[i].getSession().getValue()
      changed();
    });

    ta[i].classList.add('hide');
    // Fullscreen toggle
    document.getElementById('tfs_' + ta[i].id).setAttribute('data-id', 'ace_' + ta[i].id);

    // textarea on change, keyup | input : update ace session value
    ta[i].addEventListener('change', function(e) {
      aceEdit[i].session.setValue(e.target.value); // this.value
    });

    // Empty ta, no need set ace content
    // aceEdit[i].session.setValue(ta[i].value);

    /* --- load get snippet from local json --- */

    // A or B (Old or New in first)
    const btnOrders = {'a':['old','new'],'b':['new','old']};
    const jsonNames = [
      'ai_response-' + btnOrders[ta[i].id][0],
      'ai_response-' + btnOrders[ta[i].id][1],
      'ai_request',
      'refactor_plan'
    ];
    for (const ijs in jsonNames) {
      const respName = jsonNames[ijs].split('-');
      const jsonName = respName[0];
      const goodName = jsonName.split('_');
      const tinyName = (1 in respName) ? respName[1] : '';
      const snipName = '' + (tinyName ? tinyName + '_' : '') + 'snippet';
      const btnttj = document.createElement('button');
      btnttj.id = 'tog_tj_' + jsonName + '_' + ta[i].id + '';
      btnttj.setAttribute('data-json',jsonName);
      btnttj.setAttribute('data-snip', snipName);

      btnttj.title = 'Load ' + snipName +' from ' + jsonName + ' on diff (' + ta[i].id + ')';
      btnttj.textContent = '🔨 ' + (tinyName || goodName[1]); // '📝 ' + jsonName todo: beautify -by css-?
      btnttj.className = 'btn-tiny btn-ttj';

      btnttj.onclick = function(e) {

        // Attempt to search in parents to get meta file, start
        const node = getSnippetParent(this || e.target), // #cardX : snippet .card parent
        oId        = this.id.split('_').pop(),
        json       = this.getAttribute('data-json'),
        meta       = node.querySelector('.meta'), // document.querySelector('#card' + node.id + ' .meta'),
        file       = meta.getAttribute('data-file'),
        start      = meta.getAttribute('data-start_line');

        // getSnippetFrom(this, 'refactor_plan', 'interia_quality/doctor/latex_galaxy.py', 84);
        getSnippetFrom(this, json, file, start);
      };

      ta[i].insertAdjacentElement(position, btnttj);
    }

    const button = document.createElement('button');
    button.id = 'copy_' + ta[i].id + '';
    button.textContent = '🌈 Copy code';
    button.className = 'iiasrcta copy-button sticky';

    button.addEventListener('click', (e) => {
      const ta = document.querySelector('#' + e.target.id.replace('copy_',''));
      const btn = e.target;
      navigator.clipboard.writeText(ta.value)
        .then(() => {showNotification(btn)})
        .catch(err => {console.error('⚠️ Copy fail: ', err);});
    });
    ta[i].insertAdjacentElement(position, button);
  }
  console.log("🎯 Diff + Ace's loaded!");
});

function getSnippetParent(node) {
  if(node.id) {
    // get card ID (Only with number & >= 0)
    const cId = node.id.match(/card(\d+)/); // null | array
    if(cId && ! isNaN(cId[1]) && cId[1] > -1) return node;
  }
  node = getParent(node);
  if(!node) return false;
  return getSnippetParent(node); // searchparent
}
function getParent(node) {
  return node.parentNode || false;
}

// Tweak to set value on .hide Ace. & set first line number
// When ace is display:none Seem no update! visibility:hidden Ok
async function aceEditSetValue(aceEditor, strVal, intNumFirst) {
  const aEditIsOff = aceEditor.container.classList.contains('hide'),
    o = intNumFirst ? {firstLineNumber: intNumFirst}: 0;
  if(aEditIsOff) {
    console.log('🔎 --- Load snippet in -not display- Ace');
    aceEditor.container.style = 'visibility:hidden;min-height:0px;height:0px';
    aceEditor.container.classList.toggle('hide');
    aceEditor.session.setValue(strVal); // pins
    if(o) aceEditor.setOptions(o);      // 1st line
    await delay(200);
    console.log("Waited 200ms");
    aceEditor.container.classList.toggle('hide');
    aceEditor.container.style = '';
  } else {
    aceEditor.session.setValue(strVal); // pins
    if(o) aceEditor.setOptions(o);      // 1st line
  }
}

async function getSnippetFrom(btn, json, file, start) {
  const snip = btn.getAttribute('data-snip');
  let data,
  run    = json.replace('response', 'request').replace('_', '-'),
  btnstr = '🔧 Not find!',
  str    = '⚠️ No `'+snip+'` found in `'+json+'.json`!',
  time   = 3000; // Default
  try {
    data = await loadJSON(json + '.json'); // ai_response, refactor_plan, ai_request
  } catch {
    btnstr = '❌ Fail!';
    str = '❌ ' +json + '.json not found. 💡 Run `' + run + '` first.';
    time = 10000;
    showNotification(btn, btnstr, str, time);
    return '';
  }

  if (!data) {
    btnstr = '❓ data!';
    str = '❓ `' +json + '.json` No data! 💡 Run `' + run + '` first.';
    time = 5000;
    showNotification(btn, btnstr, str, time);
    return '';
  }

  // json ok, get where "paste" snippet
  let nId    = btn.id.split('_').pop();
  const nSrc = document.getElementById(nId); // a or b
  const tSrc = typeof(nSrc.value) == 'string' ? 'input' : 'text'; // Check is an input (idea)
  // get Snippet of ai_request--- data Shift to suggestions
  if(json == 'ai_request') {
    data = data.suggestions;
  }

  const startOk = parseInt(start) > 0; // start is num
  let stop = ! startOk; // false if line start != "?"
  dance: // How to break nested loops in JavaScript
  for (const key in data) {
    const ar = data[key];
    for (const ks in ar) {
      const obj = ar[ks];
      // start is int
      if (startOk) {
        // ai_response!stop &&
        if (typeof obj.location != 'undefined') {
          if (parseInt(obj.location?.start_line) == start) {
            stop = "🟢 - Object";
          }
          else if (typeof obj.location == 'string' && parseInt(obj.location.match(/(\d+)/g)[0]) == start) {
            stop = "🔶 - String";
          }
          else if (obj.location[0] == start) {
            stop = "🔮 - Array";
          }
        }
        // lines: ai_request, refactor_plan (python...)
        else if (typeof obj.lines != 'undefined') {
          if (obj.lines[0] == start) {
            stop = "🔵 - Array";
          }
        }
        // line: ai_request, refactor_plan (latex, md)
        else if (typeof obj.line != 'undefined') {
          if (obj.line == start) {
            stop = "🔵 - Int";
          }
        }
      }
      else { // start is "?" attempt with filename
        stop = true;
      }
      if (stop && obj.file == file) {
        btnstr = '🔍 Loaded!',
        str = '🎯 `'+snip+'` of `'+file+'`\nloaded from `'+json+'.json`', // ?
        time = 5000;
        // textarea or html tag (pre)
        // obj.(old_|new_)snippet; ~ **In js** `let value = obj.{objectPropertyName};`. It's possible like php `{$varName}`?
        const type = typeof(obj[snip]),
          pins = obj[snip] || snip + ' is ' + (type == 'string' ? 'empty' : type);
        if(tSrc=='input') {
          nSrc.value = pins;
          // Load snippet in good aceEdit
          for(let e = 0; e < aceEdit.length; e++){
            if(aceEdit[e].container.id == 'ace_' + nSrc.id) {
              // Fix no update when ace is display:none (tweak)
              aceEditSetValue(aceEdit[e], nSrc.value, start); // pins
              aceModeAuto(file, aceEdit[e]); // setMode
              break;
            }
          }
        }
        else nSrc.textContent = pins;
        changed(file);
        console.log(stop.replace("-", "--- getSnippetFrom: get start line: " + start + " in") + " of " + key + "[" + ks + "] in JSON: " + json);
        // stackoverflow.com/questions/1564818/ddg#1564838
        break dance;
      }
    }
  }
  showNotification(btn, btnstr, str, time);
}
// End getSnippetFrom

/* --- JSON Editor --- */

addJsInDom('https://bgrins.github.io/filereader.js/filereader.js', 'afterbegin', true, true); // (h, 'beforeend', true, true);
console.log("🧩 filereaderjs on load");
addJsInDom('https://cdnjs.cloudflare.com/ajax/libs/FileSaver.js/2014-11-29/FileSaver.min.js', 'afterbegin', true, true); // (h, 'beforeend', true, true);
console.log("🧩 FileSaverjs on load");


// import { createJSONEditor } from 'vanilla-jsoneditor/standalone.js'

// Or use it through a CDN (not recommended for use in production):
// import { createJSONEditor } from 'https://unpkg.com/vanilla-jsoneditor/standalone.js'
import { createJSONEditor } from 'https://cdn.jsdelivr.net/npm/vanilla-jsoneditor/standalone.js'

console.log("🧩 JSONeditor standalone js init!");

let contentjedit = {
  text: undefined,
  json: '' // undefined == Error: Content must contain either a property "json" or a property "text"
}

const jedit = createJSONEditor({
  target: document.getElementById('jsoneditor'),
  props: {
    contentjedit,
    onChange: (updatedContent, previousContent, { contentErrors, patchResult }) => {
      // contentjedit is an object { json: unknown } | { text: string }
      // console.log('JSONEditor onChange', { updatedContent, previousContent, contentErrors, patchResult })
      contentjedit = updatedContent
    }
  }
})

// use methods get, set, update, and onChange to get data in or out of the editor.
// Use updateProps to update properties.

function logContent() {
  const jsonData = jedit.get(); // Retrieve current content of jedit (jsoneditor)
  // console.log('JSONEditor Current JSON Data:', jsonData, jedit);
}

function handleChange(updatedContent) {
  // console.log('JSONEditor Updated Content:', updatedContent, jedit);
  contentjedit = updatedContent; // Setting the new content / Updating content upon change
}

window.addEventListener('load', function () {
  // Load a JSON document
  FileReaderJS.setupInput(document.getElementById('loadDocumentjedit'), {
    readAsDefault: 'Text',
    on: {
      load: function (event, file) {
        // jedit.setText(event.target.result) // jsoneditor classic
        jedit.set({text: undefined, json: JSON.parse(event.target.result)});
      }
    }
  })
  console.log("🧩 FileReaderJS loaded!");

  // Save a JSON document
  document.getElementById('saveDocumentjedit').onclick = function () {
    // Save Dialog
    let fname = window.prompt("Save as...")

    // Check json extension in file name
    if (fname.indexOf(".") === -1) {
      fname = fname + ".json"
    } else {
      if (fname.split('.').pop().toLowerCase() === "json") {
        // Nothing to do
      } else {
        fname = fname.split('.')[0] + ".json"
      }
    }
    const content = jedit.get(); // get text, json
    const blob = new Blob([JSON.stringify(content.json)], {type: 'application/json;charset=utf-8'})
    saveAs(blob, fname)
  }
})
console.log("🔑 JSONeditor loaded!");
