/* ============================================================
   Fantastic Felix Detective — Shared Rewards / Progress System
   大侦探 Felix · 侦探游戏奖励与闯关系统（共享脚本）
   所有 case 页面与奖励墙都引用这一份。改奖励只改这里。
   离线 file:// 同目录下可用。进度存浏览器 localStorage。
   ============================================================ */
(function (global) {
  'use strict';

  // ---- 奖励清单（共 28 个，编号 = 案件号）----
  var REWARDS = [
    { id: 1,  icon: '🔍', name: 'Magnifying Glass',    zh: '放大镜' },
    { id: 2,  icon: '📓', name: 'Detective Notebook',  zh: '侦探笔记本' },
    { id: 3,  icon: '🖊️', name: 'Sleuth Pen',          zh: '侦探钢笔' },
    { id: 4,  icon: '📁', name: 'File Folder',          zh: '案件文件夹' },
    { id: 5,  icon: '📏', name: 'Evidence Ruler',       zh: '证物尺子' },
    { id: 6,  icon: '🔦', name: 'Flashlight',           zh: '手电筒' },
    { id: 7,  icon: '🎙️', name: 'Voice Recorder',       zh: '录音机' },
    { id: 8,  icon: '📷', name: 'Proof Camera',         zh: '照相机' },
    { id: 9,  icon: '🗺️', name: 'Mystery Map',          zh: '神秘地图' },
    { id: 10, icon: '🧭', name: 'Direction Compass',    zh: '指南针' },
    { id: 11, icon: '🔭', name: 'Far-Away Finder',      zh: '远距离观察镜' },
    { id: 12, icon: '🖐️', name: 'Fingerprint Kit',      zh: '指纹采集套装' },
    { id: 13, icon: '🎖️', name: 'Detective Badge',      zh: '侦探徽章' },
    { id: 14, icon: '🕵️', name: 'Disguise Kit',         zh: '伪装套装' },
    { id: 15, icon: '🔑', name: 'Skeleton Key',         zh: '万能钥匙' },
    { id: 16, icon: '💍', name: 'Decoder Ring',         zh: '密码戒指' },
    { id: 17, icon: '🧪', name: 'Invisible Ink',        zh: '隐形墨水' },
    { id: 18, icon: '🏷️', name: 'Evidence Tags',        zh: '证物标签' },
    { id: 19, icon: '💼', name: 'Detective Briefcase',  zh: '侦探手提箱' },
    { id: 20, icon: '⌚', name: 'Sleuth Watch',         zh: '侦探手表' },
    { id: 21, icon: '🎩', name: 'Detective Hat',        zh: '侦探帽' },
    { id: 22, icon: '📎', name: 'Clue Clips',           zh: '线索回形针' },
    { id: 23, icon: '💡', name: 'UV Blacklight',        zh: '紫外线灯' },
    { id: 24, icon: '🪏', name: 'Clue Digger',          zh: '小铲子' },
    { id: 25, icon: '🛍️', name: 'Evidence Bag',         zh: '证物袋' },
    { id: 26, icon: '🔗', name: 'Culprit Cuffs',       zh: '手铐' },
    { id: 27, icon: '📱', name: 'Partner Phone',        zh: '对讲机' },
    { id: 28, icon: '🔱', name: 'Guardian Multi-Tool',  zh: 'Felix 的多功能防身器（终极纪念奖）',
      features: ['🔊 超响警报器 —— 一按 120 分贝，吓退坏人、呼叫伙伴',
                 '🔦 强光灯 —— 瞬间晃眼，趁机脱身',
                 '🪢 捕网发射 —— 罩住逃跑的嫌疑人',
                 '🪝 抓钩飞索 —— 翻墙越障、收回证物',
                 '🛡️ 护盾模式 —— 一键展开挡板护住自己'] }
  ];

  var STORE_KEY = 'felix_detective_rewards'; // 已解锁奖励 = 已破案件编号数组
  var TOTAL = REWARDS.length;               // 28

  // ---- 进度读写 ----
  function getUnlocked() {
    try {
      var raw = localStorage.getItem(STORE_KEY);
      var arr = raw ? JSON.parse(raw) : [];
      return Array.isArray(arr) ? arr : [];
    } catch (e) { return []; }
  }
  function isSolved(caseNumber) {
    return getUnlocked().indexOf(caseNumber) !== -1;
  }
  function unlockReward(caseNumber) {
    var unlocked = getUnlocked();
    if (unlocked.indexOf(caseNumber) === -1) {
      unlocked.push(caseNumber);
      unlocked.sort(function (a, b) { return a - b; });
      try { localStorage.setItem(STORE_KEY, JSON.stringify(unlocked)); } catch (e) {}
    }
    return REWARDS[caseNumber - 1];
  }
  function getUnlockedRewards() {
    return getUnlocked().map(function (n) { return REWARDS[n - 1]; });
  }
  function totalSolved() { return getUnlocked().length; }
  function allComplete() { return totalSolved() >= TOTAL; }

  // ---- 闯关：第 N 案是否可玩（第 1 案永远开放；其余需破完前一案）----
  function isCaseUnlocked(caseNumber) {
    return caseNumber <= 1 || isSolved(caseNumber - 1);
  }

  // ---- 文件名约定 ----
  function caseFile(n) {
    return 'detective_case_file_' + String(n).padStart(2, '0') + '.html';
  }

  // ---- 奖励弹窗（破案时调用）。挂到 <body>，不受页面缩放影响 ----
  function showRewardToast(reward, opts) {
    opts = opts || {};
    if (!reward) return;
    var overlay = document.createElement('div');
    overlay.setAttribute('style', [
      'position:fixed', 'inset:0', 'z-index:99999',
      'display:flex', 'align-items:center', 'justify-content:center',
      'background:rgba(44,36,22,0.55)', 'font-family:Georgia,serif',
      'opacity:0', 'transition:opacity .3s ease'
    ].join(';'));

    var done = totalSolved();
    var card = document.createElement('div');
    card.setAttribute('style', [
      'background:#f5f0e1', 'border:3px solid #2c2416', 'border-radius:10px',
      'box-shadow:6px 6px 0 rgba(44,36,22,0.35)', 'padding:28px 34px',
      'text-align:center', 'max-width:360px', 'transform:scale(.7) rotate(-2deg)',
      'transition:transform .35s cubic-bezier(.34,1.56,.64,1)'
    ].join(';'));
    card.innerHTML =
      '<div style="font-size:13px;letter-spacing:2px;color:#b83a2a;font-weight:bold;">REWARD UNLOCKED · 解锁奖励</div>' +
      '<div style="font-size:72px;line-height:1.2;margin:10px 0;">' + reward.icon + '</div>' +
      '<div style="font-size:22px;font-weight:bold;color:#2c2416;">' + reward.name + '</div>' +
      '<div style="font-size:14px;color:#6b4e3d;margin-top:4px;">' + reward.zh.replace('（', '<br>（') + '</div>' +
      '<div style="margin-top:16px;font-size:13px;color:#6b4e3d;">收集进度 ' + done + ' / ' + TOTAL + '</div>' +
      '<button id="rwToastClose" style="margin-top:18px;background:#b83a2a;color:#f5f0e1;border:2px solid #2c2416;border-radius:6px;padding:8px 22px;font-family:Georgia,serif;font-size:15px;cursor:pointer;box-shadow:2px 2px 0 rgba(44,36,22,0.35);">收下！</button>';

    overlay.appendChild(card);
    document.body.appendChild(overlay);
    requestAnimationFrame(function () {
      overlay.style.opacity = '1';
      card.style.transform = 'scale(1) rotate(-2deg)';
    });

    function close() {
      overlay.style.opacity = '0';
      setTimeout(function () { overlay.remove(); if (opts.onClose) opts.onClose(); }, 300);
    }
    card.querySelector('#rwToastClose').addEventListener('click', close);
    overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });

    // 读出奖励名（若浏览器支持）
    try {
      if ('speechSynthesis' in global) {
        var u = new SpeechSynthesisUtterance('You earned the ' + reward.name + '!');
        u.lang = 'en-US'; u.rate = 0.9;
        global.speechSynthesis.cancel();
        global.speechSynthesis.speak(u);
      }
    } catch (e) {}
  }

  // ---- 导出 ----
  global.DetectiveRewards = {
    REWARDS: REWARDS,
    TOTAL: TOTAL,
    STORE_KEY: STORE_KEY,
    getUnlocked: getUnlocked,
    getUnlockedRewards: getUnlockedRewards,
    isSolved: isSolved,
    unlockReward: unlockReward,
    totalSolved: totalSolved,
    allComplete: allComplete,
    isCaseUnlocked: isCaseUnlocked,
    caseFile: caseFile,
    showRewardToast: showRewardToast
  };
})(window);
