/**
 * Stop & Shop Coupon Clipper - Bookmarklet Version
 *
 * SETUP:
 * 1. Create a new bookmark in your browser
 * 2. Name it "Clip All Coupons"
 * 3. For the URL, paste the minified version below (the one starting with "javascript:")
 *
 * USAGE:
 * 1. Go to https://www.stopandshop.com/coupons
 * 2. Make sure you are logged in
 * 3. Click the bookmark
 * 4. It will scroll, load, and clip all coupons automatically
 */

// ── Copy everything below this line as the bookmark URL ──────────────

javascript:void(function(){var d=800,s=document,w=window,clipped=0,failed=0,sels=['button[aria-label*="Load to card"]','button[aria-label*="load to card"]','button[aria-label*="Clip"]','button[aria-label*="clip"]','button[data-testid*="clip"]','button[data-testid*="load-to-card"]','.coupon-clip-button:not(.clipped)','.load-to-card-button:not(.clipped)'];function sleep(ms){return new Promise(r=>setTimeout(r,ms))}function findBtns(){var r=new Set;sels.forEach(function(sel){try{s.querySelectorAll(sel).forEach(function(b){if(!b.disabled){var t=b.textContent.toLowerCase();if(!t.includes('clipped')&&!t.includes('added'))r.add(b)}})}catch(e){}});return[...r]}var box=s.createElement('div');box.style.cssText='position:fixed;top:10px;right:10px;z-index:999999;background:#fff;border:2px solid #e31837;border-radius:10px;padding:14px;font:14px Arial;box-shadow:0 4px 16px rgba(0,0,0,.2);min-width:280px';box.innerHTML='<b style="color:#e31837">Coupon Clipper</b><div id="ccstat" style="margin:8px 0;font-size:13px">Starting...</div>';s.body.appendChild(box);var stat=s.getElementById('ccstat');async function run(){stat.textContent='Scrolling to load all coupons...';var prev=0,tries=0;while(tries<30){w.scrollTo(0,s.body.scrollHeight);await sleep(1500);var h=s.body.scrollHeight;if(h===prev)break;prev=h;tries++;stat.textContent='Loading... (scroll '+tries+')'}w.scrollTo(0,0);await sleep(1000);var btns=findBtns();stat.textContent='Found '+btns.length+' coupons. Clipping...';for(var i=0;i<btns.length;i++){try{btns[i].scrollIntoView({behavior:'smooth',block:'center'});await sleep(300);btns[i].click();clipped++;stat.textContent='Clipping: '+clipped+'/'+btns.length}catch(e){failed++}await sleep(d)}stat.textContent='Done! Clipped: '+clipped+' | Failed: '+failed;setTimeout(function(){box.remove()},15000)}run()})();
