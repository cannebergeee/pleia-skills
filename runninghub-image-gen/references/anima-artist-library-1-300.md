# Anima 画师知识库（1-300）

用于 RunningHub `anima*` / `oldanima*` 工作流的画师选择。数据来自 ASR Ranker 前 300 名，并以 Danbooru artist 记录优先核实身份与别名。

## 使用规则

- 在需要为 Anima 选择、替换、组合画师时读取本文件；用户没有明确画师要求时也读取本文件。
- 使用 `name` 列进入 prompt，必须保留 `@` 前缀，并把下划线写成空格。
- 默认只选 1 位画师；用户没有明确指定画师时，从全量表 **rank 1-200** 中随机选择 1 位。用户明确要求混合风格时最多选 2 位。
- 优先使用 `confidence=high` 或 `medium`；`low` 仅在用户明确点名或没有更好选择时使用。
- Danbooru 主要用于确认画师身份和别名；`style` / `usage` 是给 Anima 选风格的实用概括，不是 Danbooru 原文。
- `danbooru_status=not_found` 的条目仍可用，但应视为待复核。

## 快速选择

| 需求 | 优先画师 | 说明 |
|------|----------|------|
| 默认稳定日系角色 | `@mozukuzu (manukedori)`, `@ixy`, `@nagi ryou` | 清晰线稿、角色稳定 |
| 明亮萌系/可爱少女 | `@ixy`, `@hamao`, `@ningen mame`, `@gale kawaii` | 可爱、明亮、头像和日常好用 |
| 华丽幻想/古风 | `@ibuki satsuki`, `@lingyi`, `@seno (senohime)` | 服饰、幻想角色、精美立绘 |
| 半写实/厚涂氛围 | `@guweiz`, `@anato finnstark`, `@gsusart`, `@krekkov` | 强光影、电影感或暗黑幻想 |
| 游戏/galgame 立绘 | `@wada arco`, `@mino tarou`, `@bekkankou`, `@ssambatea` | 角色设计、商业插画、立绘 |
| 科幻/机械角色 | `@neco` | 机甲、战斗服、未来感 |

## 全量表

| Rank | 画师 | Score | Uncertainty | 风格 | 适用 | Confidence | Danbooru |
|------|------|-------|-------------|------|------|------------|----------|
| 1 | `@mozukuzu (manukedori)` | 43 | ±2 | 柔和日系、细腻线稿、轻透明上色 | 少女、东方系、清爽角色图 | medium | [mozukuzu_(manukedori)](https://danbooru.donmai.us/artists/32011) |
| 2 | `@ibuki satsuki` | 42 | ±3 | 华丽幻想、精细服饰、东方奇幻色彩 | 古风、幻想角色、精美立绘 | high | [ibuki_satsuki](https://danbooru.donmai.us/artists/285433) |
| 3 | `@kuinji 51go` | 41 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [kuinji_51go](https://danbooru.donmai.us/artists/44993) |
| 4 | `@hjl` | 41 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [hjl](https://danbooru.donmai.us/artists/61717) |
| 5 | `@kagoya1219` | 41 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [kagoya1219](https://danbooru.donmai.us/artists/258753) |
| 6 | `@dizi930` | 40 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [dizi930](https://danbooru.donmai.us/artists/96980) |
| 7 | `@navy (navy.blue)` | 39 | ±3 | 清爽蓝调、细腻日系、柔和光影 | 清新少女、校园、夏日感 | medium | [navy_(navy.blue)](https://danbooru.donmai.us/artists/100931) |
| 8 | `@minowa sukyaru` | 39 | ±2 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [minowa_sukyaru](https://danbooru.donmai.us/artists/106872) |
| 9 | `@gogalking` | 39 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [gogalking](https://danbooru.donmai.us/artists/194706) |
| 10 | `@ppap (11zhakdpek19)` | 39 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [ppap_(11zhakdpek19)](https://danbooru.donmai.us/artists/220357) |
| 11 | `@ningen mame` | 39 | ±2 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [ningen_mame](https://danbooru.donmai.us/artists/230123) |
| 12 | `@ouhara lolong` | 39 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [ouhara_lolong](https://danbooru.donmai.us/artists/111289) |
| 13 | `@yue (shemika98425261)` | 38 | ±2 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | medium | [yue_(shemika98425261)](https://danbooru.donmai.us/artists/260061) |
| 14 | `@quasarcake` | 38 | ±2 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [quasarcake](https://danbooru.donmai.us/artists/241140) |
| 15 | `@ixy` | 37 | ±3 | 明亮可爱、干净线稿、萌系高辨识度 | 萌系、偶像、轻快商业插画 | high | [ixy](https://danbooru.donmai.us/artists/4758) |
| 16 | `@dorontabi` | 37 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [dorontabi](https://danbooru.donmai.us/artists/207254) |
| 17 | `@cofffee` | 37 | ±4 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [cofffee](https://danbooru.donmai.us/artists/224114) |
| 18 | `@asutora` | 37 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [asutora](https://danbooru.donmai.us/artists/74532) |
| 19 | `@toucailao` | 36 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | low | not_found |
| 20 | `@machiko (beard)` | 36 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [machiko_(beard)](https://danbooru.donmai.us/artists/12575) |
| 21 | `@herio` | 36 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [herio](https://danbooru.donmai.us/artists/47177) |
| 22 | `@mi (pic52pic)` | 36 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [mi_(pic52pic)](https://danbooru.donmai.us/artists/159160) |
| 23 | `@donguri suzume` | 36 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [donguri_suzume](https://danbooru.donmai.us/artists/149062) |
| 24 | `@jyt` | 36 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [jyt](https://danbooru.donmai.us/artists/131418) |
| 25 | `@gaston18` | 36 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [gaston18](https://danbooru.donmai.us/artists/100381) |
| 26 | `@c.honey` | 35 | ±3 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [c.honey](https://danbooru.donmai.us/artists/146428) |
| 27 | `@gsusart` | 35 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [gsusart](https://danbooru.donmai.us/artists/295680) |
| 28 | `@fushirun rung` | 35 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [fushirun_rung](https://danbooru.donmai.us/artists/285922) |
| 29 | `@krekkov` | 35 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [krekkov](https://danbooru.donmai.us/artists/191623) |
| 30 | `@inaeda kei` | 35 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | low | not_found |
| 31 | `@inu totemo` | 35 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | low | not_found |
| 32 | `@k00s` | 35 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [k00s](https://danbooru.donmai.us/artists/236340) |
| 33 | `@yogisya` | 35 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [yogisya](https://danbooru.donmai.us/artists/46568) |
| 34 | `@renge (730)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [renge_(730)](https://danbooru.donmai.us/artists/258740) |
| 35 | `@hamao` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [hamao](https://danbooru.donmai.us/artists/7961) |
| 36 | `@ushimittsu` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [ushimittsu](https://danbooru.donmai.us/artists/190286) |
| 37 | `@hoshino ouka` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [hoshino_ouka](https://danbooru.donmai.us/artists/90279) |
| 38 | `@tsumeki` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [tsumeki](https://danbooru.donmai.us/artists/193006) |
| 39 | `@wulazula` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [wulazula](https://danbooru.donmai.us/artists/130191) |
| 40 | `@temu (temp mumu)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [temu_(temp_mumu)](https://danbooru.donmai.us/artists/440371) |
| 41 | `@suenari (peace)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [suenari_(peace)](https://danbooru.donmai.us/artists/87564) |
| 42 | `@sempon (doppio note)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [sempon_(doppio_note)](https://danbooru.donmai.us/artists/144522) |
| 43 | `@ken'ichi (ken1ro u)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [kenichi](https://danbooru.donmai.us/artists/493797) |
| 44 | `@nao (syn eaa)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [nao_(syn_eaa)](https://danbooru.donmai.us/artists/143840) |
| 45 | `@gale kawaii` | 34 | ±3 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [gale_kawaii](https://danbooru.donmai.us/artists/117936) |
| 46 | `@yutamaro` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [yutamaro](https://danbooru.donmai.us/artists/60799) |
| 47 | `@28 (282teeth)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [28_(282teeth)](https://danbooru.donmai.us/artists/263710) |
| 48 | `@shiwo (siwosi)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [shiwo_(siwosi)](https://danbooru.donmai.us/artists/102636) |
| 49 | `@natsu (rodysanp)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [natsu_(rodysanp)](https://danbooru.donmai.us/artists/217500) |
| 50 | `@die (die0118)` | 34 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | low | not_found |
| 51 | `@uenomigi` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [uenomigi](https://danbooru.donmai.us/artists/265090) |
| 52 | `@iroiro yaru hito` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [iroiro_yaru_hito](https://danbooru.donmai.us/artists/110508) |
| 53 | `@tima` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [tima](https://danbooru.donmai.us/artists/16553) |
| 54 | `@nakareki` | 33 | ±4 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [nakareki](https://danbooru.donmai.us/artists/127502) |
| 55 | `@reki (user rcrd4534)` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | low | not_found |
| 56 | `@nahanmin` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [nahanmin](https://danbooru.donmai.us/artists/186724) |
| 57 | `@mignon` | 33 | ±3 | 精致美少女、柔光、皮肤质感强 | 美少女、头像、商业插画 | high | [mignon](https://danbooru.donmai.us/artists/25424) |
| 58 | `@vanripper` | 33 | ±3 | 扁平漫画感、粗线条、黑白红强对比 | 漫画角色、表情、风格化角色 | high | [vanripper](https://danbooru.donmai.us/artists/204663) |
| 59 | `@speedl00ver` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [speedl00ver](https://danbooru.donmai.us/artists/275461) |
| 60 | `@wada arco` | 33 | ±3 | 鲜艳扁平、装饰性强、Fate 系辨识度 | 游戏角色、明快主视觉、夸张表情 | high | [wada_arco](https://danbooru.donmai.us/artists/7260) |
| 61 | `@raikoart` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [raikoart](https://danbooru.donmai.us/artists/122637) |
| 62 | `@lingyi` | 33 | ±3 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | medium | [lingyi](https://danbooru.donmai.us/artists/309672) |
| 63 | `@mabing` | 33 | ±4 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [mabing](https://danbooru.donmai.us/artists/209084) |
| 64 | `@shiren (ourboy83)` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [shiren_(ourboy83)](https://danbooru.donmai.us/artists/268577) |
| 65 | `@hijiki (hijikini)` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [hijiki_(hijikini)](https://danbooru.donmai.us/artists/11141) |
| 66 | `@kikumaru bunta` | 33 | ±3 | 高完成度日系角色、清晰线稿、稳定上色 | 默认泛用、角色立绘、头像、同人插画 | medium | [kikumaru_bunta](https://danbooru.donmai.us/artists/5271) |
| 67 | `@haun` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [haun](https://danbooru.donmai.us/artists/65457) |
| 68 | `@shone` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [shone](https://danbooru.donmai.us/artists/94280) |
| 69 | `@casino (casinoep)` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [casino_(casinoep)](https://danbooru.donmai.us/artists/118516) |
| 70 | `@kawakami rokkaku` | 32 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [kawakami_rokkaku](https://danbooru.donmai.us/artists/42189) |
| 71 | `@kaifei (kaifei 29)` | 32 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [kaifei_(kaifei_29)](https://danbooru.donmai.us/artists/76626) |
| 72 | `@rippajun` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [rippajun](https://danbooru.donmai.us/artists/221809) |
| 73 | `@tsukasa tsubasa` | 32 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [tsukasa_tsubasa](https://danbooru.donmai.us/artists/181920) |
| 74 | `@chorogon` | 32 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [chorogon](https://danbooru.donmai.us/artists/194694) |
| 75 | `@yuzuyomogi` | 32 | ±3 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [yuzuyomogi](https://danbooru.donmai.us/artists/72392) |
| 76 | `@bai qi-qsr` | 32 | ±3 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | low | not_found |
| 77 | `@misheng liu yin` | 32 | ±3 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | medium | [misheng_liu_yin](https://danbooru.donmai.us/artists/248073) |
| 78 | `@wamudraws` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [wamudraws](https://danbooru.donmai.us/artists/202145) |
| 79 | `@fujikawa daichi` | 32 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [fujikawa_daichi](https://danbooru.donmai.us/artists/7559) |
| 80 | `@pechika` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [pechika](https://danbooru.donmai.us/artists/23290) |
| 81 | `@namihaya` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [namihaya](https://danbooru.donmai.us/artists/100224) |
| 82 | `@onono imoko` | 32 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [onono_imoko](https://danbooru.donmai.us/artists/6554) |
| 83 | `@ka (marukogedago)` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [ka](https://danbooru.donmai.us/artists/469210) |
| 84 | `@tsukimi 50` | 32 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [tsukimi_50](https://danbooru.donmai.us/artists/113600) |
| 85 | `@quan (kurisu tina)` | 32 | ±3 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | medium | [quan_(kurisu_tina)](https://danbooru.donmai.us/artists/126950) |
| 86 | `@aoi suzu` | 32 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [aoi_suzu](https://danbooru.donmai.us/artists/158185) |
| 87 | `@tama (tama-s)` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [tama_(tama-s)](https://danbooru.donmai.us/artists/152469) |
| 88 | `@daeho cha` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [daeho_cha](https://danbooru.donmai.us/artists/97463) |
| 89 | `@bacun` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [bacun](https://danbooru.donmai.us/artists/171246) |
| 90 | `@spirytus tarou` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [spirytus_tarou](https://danbooru.donmai.us/artists/90001) |
| 91 | `@umiroku` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [umiroku](https://danbooru.donmai.us/artists/102814) |
| 92 | `@atychi` | 31 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [atychi](https://danbooru.donmai.us/artists/158853) |
| 93 | `@rucchiifu` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [rucchiifu](https://danbooru.donmai.us/artists/113364) |
| 94 | `@guweiz` | 31 | ±3 | 油画感半写实、氛围强、暗调光影 | 风景、意境、电影感角色 | high | [guweiz](https://danbooru.donmai.us/artists/122964) |
| 95 | `@medinki` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [medinki](https://danbooru.donmai.us/artists/41147) |
| 96 | `@yusan` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [yusan](https://danbooru.donmai.us/artists/124598) |
| 97 | `@saberiii` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [saberiii](https://danbooru.donmai.us/artists/57268) |
| 98 | `@tsukiori` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [tsukiori](https://danbooru.donmai.us/artists/82733) |
| 99 | `@pikurusu` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [pikurusu](https://danbooru.donmai.us/artists/129390) |
| 100 | `@ikura hato` | 31 | ±4 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [ikura_hato](https://danbooru.donmai.us/artists/4873) |
| 101 | `@seno (senohime)` | 31 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [seno_(senohime)](https://danbooru.donmai.us/artists/160437) |
| 102 | `@anato finnstark` | 31 | ±3 | 暗黑奇幻、电影感、史诗环境光 | 黑暗幻想、概念场景、氛围图 | high | [anato_finnstark](https://danbooru.donmai.us/artists/144857) |
| 103 | `@plus2sf` | 31 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [plus2sf](https://danbooru.donmai.us/artists/398326) |
| 104 | `@seungju lee` | 31 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [seungju_lee](https://danbooru.donmai.us/artists/151847) |
| 105 | `@umeume (totoya)` | 31 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [umeume_(totoya)](https://danbooru.donmai.us/artists/200867) |
| 106 | `@torakichi (ebitendon)` | 31 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [torakichi_(ebitendon)](https://danbooru.donmai.us/artists/52797) |
| 107 | `@fuyu no usagi` | 30 | ±3 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [fuyu_no_usagi](https://danbooru.donmai.us/artists/127531) |
| 108 | `@bentouoic` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [bentouoic](https://danbooru.donmai.us/artists/467775) |
| 109 | `@saku (osake love)` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [saku_(osake_love)](https://danbooru.donmai.us/artists/52684) |
| 110 | `@cougar (cougar1404)` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [cougar_(cougar1404)](https://danbooru.donmai.us/artists/185898) |
| 111 | `@shiro youduki` | 30 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [shiro_youduki](https://danbooru.donmai.us/artists/175640) |
| 112 | `@gubbi on` | 30 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [gubbi_on](https://danbooru.donmai.us/artists/377704) |
| 113 | `@nekoi mie` | 30 | ±3 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [nekoi_mie](https://danbooru.donmai.us/artists/5128) |
| 114 | `@nagi ryou` | 30 | ±4 | 细腻日系、清透色、游戏/轻小说感 | 美少女立绘、轻小说封面 | high | [nagi_ryou](https://danbooru.donmai.us/artists/5234) |
| 115 | `@satou aji` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [satou_aji](https://danbooru.donmai.us/artists/131813) |
| 116 | `@tajima yukie` | 30 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [tajima_yukie](https://danbooru.donmai.us/artists/106622) |
| 117 | `@sumiya nadateru` | 30 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [sumiya_nadateru](https://danbooru.donmai.us/artists/97141) |
| 118 | `@saeki sora` | 30 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [saeki_sora](https://danbooru.donmai.us/artists/98093) |
| 119 | `@mameeekueya` | 30 | ±4 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | low | not_found |
| 120 | `@jikuno` | 30 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [jikuno](https://danbooru.donmai.us/artists/122706) |
| 121 | `@pote (pote 39)` | 30 | ±4 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [pote_(pote_39)](https://danbooru.donmai.us/artists/357950) |
| 122 | `@mongguri` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [mongguri](https://danbooru.donmai.us/artists/200782) |
| 123 | `@netural` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [netural](https://danbooru.donmai.us/artists/237463) |
| 124 | `@z3zz4` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [z3zz4](https://danbooru.donmai.us/artists/261471) |
| 125 | `@hitowa` | 30 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [hitowa](https://danbooru.donmai.us/artists/33268) |
| 126 | `@mino tarou` | 30 | ±3 | 清爽 galgame 系、干净线稿、明亮角色 | 恋爱游戏、校园、角色立绘 | high | [mino_tarou](https://danbooru.donmai.us/artists/124189) |
| 127 | `@tsukino (nakajimaseiki)` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [tsukino_(nakajimaseiki)](https://danbooru.donmai.us/artists/147514) |
| 128 | `@ssambatea` | 30 | ±3 | 韩系精细日系、柔和光、精美少女 | 少女、头像、商业插画 | high | [ssambatea](https://danbooru.donmai.us/artists/170722) |
| 129 | `@kinako (shiratama mochi)` | 30 | ±4 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [kinako_(shiratama_mochi)](https://danbooru.donmai.us/artists/131920) |
| 130 | `@sankuro (agoitei)` | 30 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [sankuro_(agoitei)](https://danbooru.donmai.us/artists/29889) |
| 131 | `@sanwari (aruji yume)` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [sanwari_(aruji_yume)](https://danbooru.donmai.us/artists/211263) |
| 132 | `@yamaguchi shinnosuke` | 30 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [yamaguchi_shinnosuke](https://danbooru.donmai.us/artists/5256) |
| 133 | `@kaguyuzu` | 30 | ±4 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [kaguyuzu](https://danbooru.donmai.us/artists/15337) |
| 134 | `@silverxp` | 29 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [silverxp](https://danbooru.donmai.us/artists/98150) |
| 135 | `@sukaliya` | 29 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [sukaliya](https://danbooru.donmai.us/artists/243937) |
| 136 | `@mokokoiro` | 29 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [mokokoiro](https://danbooru.donmai.us/artists/212320) |
| 137 | `@kabu usagi` | 29 | ±3 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [kabu_usagi](https://danbooru.donmai.us/artists/237010) |
| 138 | `@suzuki24` | 29 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [suzuki24](https://danbooru.donmai.us/artists/82739) |
| 139 | `@takubon` | 29 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [takubon](https://danbooru.donmai.us/artists/161811) |
| 140 | `@koyomania` | 29 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [koyomania](https://danbooru.donmai.us/artists/205681) |
| 141 | `@yunmi 0527` | 29 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [yunmi_0527](https://danbooru.donmai.us/artists/190629) |
| 142 | `@4suke` | 29 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [4suke](https://danbooru.donmai.us/artists/92926) |
| 143 | `@jacknavy` | 29 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [jacknavy](https://danbooru.donmai.us/artists/97722) |
| 144 | `@airi (akamichiaika)` | 29 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [airi_(akamichiaika)](https://danbooru.donmai.us/artists/118228) |
| 145 | `@kay yu` | 29 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [kay_yu](https://danbooru.donmai.us/artists/194155) |
| 146 | `@kuroda kazuya` | 29 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [kuroda_kazuya](https://danbooru.donmai.us/artists/54806) |
| 147 | `@megateru` | 29 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [megateru](https://danbooru.donmai.us/artists/47530) |
| 148 | `@merrytail` | 29 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [merrytail](https://danbooru.donmai.us/artists/212255) |
| 149 | `@marimo jh` | 29 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [marimo_jh](https://danbooru.donmai.us/artists/220532) |
| 150 | `@jin (oihlf)` | 29 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [jin_(oihlf)](https://danbooru.donmai.us/artists/393978) |
| 151 | `@dot r` | 29 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [dot_r](https://danbooru.donmai.us/artists/18338) |
| 152 | `@akichi 360` | 29 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [akichi_360](https://danbooru.donmai.us/artists/330432) |
| 153 | `@kangetsu (fhalei)` | 29 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [kangetsu_(fhalei)](https://danbooru.donmai.us/artists/41549) |
| 154 | `@koza game` | 29 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [koza_game](https://danbooru.donmai.us/artists/135578) |
| 155 | `@sleepy frippy` | 28 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [sleepy_frippy](https://danbooru.donmai.us/artists/153622) |
| 156 | `@jampen` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [jampen](https://danbooru.donmai.us/artists/89218) |
| 157 | `@mina cream` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [mina_cream](https://danbooru.donmai.us/artists/137902) |
| 158 | `@binggong asylum` | 28 | ±3 | 幻想/暗调倾向、厚涂或概念感 | 暗黑奇幻、氛围角色、概念图 | medium | [binggong_asylum](https://danbooru.donmai.us/artists/181410) |
| 159 | `@yqgkg` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | low | not_found |
| 160 | `@banishment` | 28 | ±4 | 幻想/暗调倾向、厚涂或概念感 | 暗黑奇幻、氛围角色、概念图 | medium | [banishment](https://danbooru.donmai.us/artists/157757) |
| 161 | `@nextoad` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [nextoad](https://danbooru.donmai.us/artists/195649) |
| 162 | `@nhaliz` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [nhaliz](https://danbooru.donmai.us/artists/117128) |
| 163 | `@shihou (g-o-s)` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [shihou_(g-o-s)](https://danbooru.donmai.us/artists/37210) |
| 164 | `@suke (singekijyosei)` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [suke_(singekijyosei)](https://danbooru.donmai.us/artists/152806) |
| 165 | `@aruka (alka p1)` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [aruka_(alka_p1)](https://danbooru.donmai.us/artists/96664) |
| 166 | `@quick waipa` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [quick_waipa](https://danbooru.donmai.us/artists/43906) |
| 167 | `@laceysx` | 28 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [laceysx](https://danbooru.donmai.us/artists/206482) |
| 168 | `@r oot` | 28 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [r_oot](https://danbooru.donmai.us/artists/254105) |
| 169 | `@miyazakisoul` | 28 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [miyazakisoul](https://danbooru.donmai.us/artists/286294) |
| 170 | `@miyabino (miyabi1616)` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [miyabino_(miyabi1616)](https://danbooru.donmai.us/artists/118220) |
| 171 | `@metatarou` | 28 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [metatarou](https://danbooru.donmai.us/artists/266171) |
| 172 | `@pokemoa` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [pokemoa](https://danbooru.donmai.us/artists/11998) |
| 173 | `@attyon` | 28 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [attyon](https://danbooru.donmai.us/artists/96926) |
| 174 | `@ia (ias1010)` | 28 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [ia_(ias1010)](https://danbooru.donmai.us/artists/161579) |
| 175 | `@sino (sionori)` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [sino_(sionori)](https://danbooru.donmai.us/artists/56906) |
| 176 | `@soranokakera01` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [soranokakera01](https://danbooru.donmai.us/artists/199899) |
| 177 | `@kisamu (ksmz)` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [kisamu_(ksmz)](https://danbooru.donmai.us/artists/109569) |
| 178 | `@trefle r` | 28 | ±3 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [trefle_r](https://danbooru.donmai.us/artists/68421) |
| 179 | `@yewang19` | 28 | ±4 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | medium | [yewang19](https://danbooru.donmai.us/artists/111326) |
| 180 | `@chela77` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [chela77](https://danbooru.donmai.us/artists/206906) |
| 181 | `@jesse (pixiv34586727)` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [jesse_(pixiv34586727)](https://danbooru.donmai.us/artists/193313) |
| 182 | `@yashiro seika` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [yashiro_seika](https://danbooru.donmai.us/artists/28302) |
| 183 | `@naotosi` | 28 | ±5 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [naotosi](https://danbooru.donmai.us/artists/224058) |
| 184 | `@void 0` | 28 | ±5 | 幻想/暗调倾向、厚涂或概念感 | 暗黑奇幻、氛围角色、概念图 | medium | [void_0](https://danbooru.donmai.us/artists/218424) |
| 185 | `@materclaws` | 28 | ±4 | 日系角色插画、柔和上色、二次元人物向 | 角色参考、头像、轻插画 | medium | [materclaws](https://danbooru.donmai.us/artists/126624) |
| 186 | `@mr.lime` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [mr.lime](https://danbooru.donmai.us/artists/174754) |
| 187 | `@bishi (bishi)` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [bishi_(bishi)](https://danbooru.donmai.us/artists/161970) |
| 188 | `@squchan` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [squchan](https://danbooru.donmai.us/artists/48205) |
| 189 | `@yuiga naoha` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [yuiga_naoha](https://danbooru.donmai.us/artists/91073) |
| 190 | `@sakura ryuuken` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [sakura_ryuuken](https://danbooru.donmai.us/artists/6123) |
| 191 | `@seafh` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [seafh](https://danbooru.donmai.us/artists/57997) |
| 192 | `@neco` | 27 | ±4 | 机械感日系、硬朗线条、未来感 | 机甲、科幻角色、战斗服 | high | [neco](https://danbooru.donmai.us/artists/79558) |
| 193 | `@mushpz` | 27 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [mushpz](https://danbooru.donmai.us/artists/162863) |
| 194 | `@hechi (hechi322)` | 27 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [hechi_(hechi322)](https://danbooru.donmai.us/artists/136383) |
| 195 | `@maririn` | 27 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [maririn](https://danbooru.donmai.us/artists/28345) |
| 196 | `@yt (wai-tei)` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [yt_(wai-tei)](https://danbooru.donmai.us/artists/59923) |
| 197 | `@makoto ikemu` | 27 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [makoto_ikemu](https://danbooru.donmai.us/artists/154315) |
| 198 | `@jesse schickler` | 27 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [jesse_schickler](https://danbooru.donmai.us/artists/194579) |
| 199 | `@hamachamu` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [hamachamu](https://danbooru.donmai.us/artists/194983) |
| 200 | `@fujishiro emyu` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [fujishiro_emyu](https://danbooru.donmai.us/artists/44027) |
| 201 | `@makicha (sasurainopink)` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [makicha_(sasurainopink)](https://danbooru.donmai.us/artists/260878) |
| 202 | `@afukuro` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [afukuro](https://danbooru.donmai.us/artists/79082) |
| 203 | `@koi (koisan)` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [koi_(koisan)](https://danbooru.donmai.us/artists/16661) |
| 204 | `@shakkiyi` | 27 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [shakkiyi](https://danbooru.donmai.us/artists/230046) |
| 205 | `@waero` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [waero](https://danbooru.donmai.us/artists/72834) |
| 206 | `@nako (unclebanana)` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [nako_(unclebanana)](https://danbooru.donmai.us/artists/100089) |
| 207 | `@warekara` | 27 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [warekara](https://danbooru.donmai.us/artists/121535) |
| 208 | `@ichiei` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [ichiei](https://danbooru.donmai.us/artists/61096) |
| 209 | `@pondel` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [pondel](https://danbooru.donmai.us/artists/202930) |
| 210 | `@shironeko yuuki` | 27 | ±4 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [shironeko_yuuki](https://danbooru.donmai.us/artists/89794) |
| 211 | `@ekz (robotekz)` | 27 | ±4 | 幻想/暗调倾向、厚涂或概念感 | 暗黑奇幻、氛围角色、概念图 | medium | [ekz_(robotekz)](https://danbooru.donmai.us/artists/138202) |
| 212 | `@qtonagi` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [qtonagi](https://danbooru.donmai.us/artists/78302) |
| 213 | `@chiri (ch!)` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [chiri](https://danbooru.donmai.us/artists/366576) |
| 214 | `@miyabi urumi` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | low | not_found |
| 215 | `@ousaka nozomi` | 27 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [ousaka_nozomi](https://danbooru.donmai.us/artists/75857) |
| 216 | `@m75255831` | 27 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [m75255831](https://danbooru.donmai.us/artists/320890) |
| 217 | `@aya shachou` | 27 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [aya_shachou](https://danbooru.donmai.us/artists/19093) |
| 218 | `@qian wu atai` | 27 | ±3 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | low | not_found |
| 219 | `@ellu` | 26 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [ellu](https://danbooru.donmai.us/artists/208133) |
| 220 | `@nishuu miri` | 26 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [nishuu_miri](https://danbooru.donmai.us/artists/148094) |
| 221 | `@shamonabe` | 26 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [shamonabe](https://danbooru.donmai.us/artists/113163) |
| 222 | `@zenrakishi` | 26 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [zenrakishi](https://danbooru.donmai.us/artists/187603) |
| 223 | `@fii fii (feefeeowo)` | 26 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [fii_fii_(feefeeowo)](https://danbooru.donmai.us/artists/142387) |
| 224 | `@matsurika youko` | 26 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [matsurika_youko](https://danbooru.donmai.us/artists/74813) |
| 225 | `@stmast` | 26 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [stmast](https://danbooru.donmai.us/artists/104069) |
| 226 | `@sonsoso` | 26 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [sonsoso](https://danbooru.donmai.us/artists/82786) |
| 227 | `@a-xii` | 26 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [a-xii](https://danbooru.donmai.us/artists/213224) |
| 228 | `@genkung` | 26 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [genkung](https://danbooru.donmai.us/artists/122064) |
| 229 | `@nyamaso` | 26 | ±5 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [nyamaso](https://danbooru.donmai.us/artists/93493) |
| 230 | `@k+` | 26 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [k+](https://danbooru.donmai.us/artists/13890) |
| 231 | `@honzawa yuuichirou` | 26 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [honzawa_yuuichirou](https://danbooru.donmai.us/artists/112367) |
| 232 | `@takashina masato` | 26 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [takashina_masato](https://danbooru.donmai.us/artists/13213) |
| 233 | `@marugoshi (54burger)` | 26 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [marugoshi_(54burger)](https://danbooru.donmai.us/artists/22160) |
| 234 | `@yuuhi homare` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [yuuhi_homare](https://danbooru.donmai.us/artists/41536) |
| 235 | `@kirisaki seeker` | 25 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [kirisaki_seeker](https://danbooru.donmai.us/artists/155496) |
| 236 | `@natsu (sinker8c)` | 25 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [natsu_(sinker8c)](https://danbooru.donmai.us/artists/118939) |
| 237 | `@kurokawa (kurokashi655)` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [kurokawa_(kurokashi655)](https://danbooru.donmai.us/artists/89241) |
| 238 | `@chengongzi123` | 25 | ±3 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | medium | [chengongzi123](https://danbooru.donmai.us/artists/217575) |
| 239 | `@kurohal` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [kurohal](https://danbooru.donmai.us/artists/71552) |
| 240 | `@ooyama imo` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [ooyama_imo](https://danbooru.donmai.us/artists/115701) |
| 241 | `@roina (effj7473)` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [roina_(effj7473)](https://danbooru.donmai.us/artists/206161) |
| 242 | `@momokumo` | 25 | ±5 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [momokumo](https://danbooru.donmai.us/artists/34846) |
| 243 | `@kodama (mmt uf)` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [kodama_(mmt_uf)](https://danbooru.donmai.us/artists/161396) |
| 244 | `@fangxiang cuoluan` | 25 | ±3 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | low | not_found |
| 245 | `@furukawa raku` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [furukawa_raku](https://danbooru.donmai.us/artists/329493) |
| 246 | `@gawako` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [gawako](https://danbooru.donmai.us/artists/318260) |
| 247 | `@hikawayunn` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [hikawayunn](https://danbooru.donmai.us/artists/307985) |
| 248 | `@keita (o4510 9chi9)` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [keita_(o4510_9chi9)](https://danbooru.donmai.us/artists/337315) |
| 249 | `@yuuyuu (yuko)` | 25 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [yuuyuu_(yuko)](https://danbooru.donmai.us/artists/16267) |
| 250 | `@ao (ao0 0nemu)` | 25 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [ao_(ao0_0nemu)](https://danbooru.donmai.us/artists/157802) |
| 251 | `@wucanming` | 25 | ±5 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | medium | [wucanming](https://danbooru.donmai.us/artists/164424) |
| 252 | `@uraki (tetsu420)` | 25 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [uraki_(tetsu420)](https://danbooru.donmai.us/artists/58225) |
| 253 | `@miyako (naotsugu)` | 25 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [miyako_(naotsugu)](https://danbooru.donmai.us/artists/82320) |
| 254 | `@bekkankou` | 25 | ±4 | 经典 galgame 原画、柔和少女、清爽色 | 校园、恋爱游戏、少女立绘 | high | [bekkankou](https://danbooru.donmai.us/artists/10165) |
| 255 | `@hekoningyou (waraningyou)` | 25 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [hekoningyou_(waraningyou)](https://danbooru.donmai.us/artists/112369) |
| 256 | `@kana (kanna runa0620)` | 25 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [kana_(kanna_runa0620)](https://danbooru.donmai.us/artists/361415) |
| 257 | `@sage (mami1210)` | 24 | ±6 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [sage_(mami1210)](https://danbooru.donmai.us/artists/39593) |
| 258 | `@nashidrop` | 24 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [nashidrop](https://danbooru.donmai.us/artists/208596) |
| 259 | `@hoe satsuki` | 24 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [hoe_satsuki](https://danbooru.donmai.us/artists/37639) |
| 260 | `@psd (psdgai)` | 24 | ±3 | 高饱和日系、精细厚涂、角色表现强 | 视觉冲击、同人主视觉、头像 | medium | [psd_(psdgai)](https://danbooru.donmai.us/artists/30531) |
| 261 | `@d futagosaikyou` | 24 | ±6 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [d_futagosaikyou](https://danbooru.donmai.us/artists/197557) |
| 262 | `@vamos mk` | 24 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [vamos_mk](https://danbooru.donmai.us/artists/342100) |
| 263 | `@emia wang` | 24 | ±4 | 华语圈日系插画、细腻上色、角色向 | 少女、古风/幻想、头像、角色立绘 | medium | [emia_wang](https://danbooru.donmai.us/artists/79600) |
| 264 | `@man (trance)` | 24 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [man_(trance)](https://danbooru.donmai.us/artists/15116) |
| 265 | `@desaku` | 24 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [desaku](https://danbooru.donmai.us/artists/60257) |
| 266 | `@niku (ni23ku)` | 24 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [niku_(ni23ku)](https://danbooru.donmai.us/artists/177661) |
| 267 | `@ashiomi masato` | 24 | ±6 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [ashiomi_masato](https://danbooru.donmai.us/artists/17910) |
| 268 | `@kuziaaizuk` | 24 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | low | not_found |
| 269 | `@shirotsumekusa` | 24 | ±3 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [shirotsumekusa](https://danbooru.donmai.us/artists/5113) |
| 270 | `@mashima saki (mashimasa)` | 24 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [mashima_saki_(mashimasa)](https://danbooru.donmai.us/artists/105241) |
| 271 | `@neko (yanshoujie)` | 24 | ±4 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [neko_(yanshoujie)](https://danbooru.donmai.us/artists/77253) |
| 272 | `@rock zinc` | 24 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [rock_zinc](https://danbooru.donmai.us/artists/293541) |
| 273 | `@monokuro (sekahate)` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [monokuro_(sekahate)](https://danbooru.donmai.us/artists/18993) |
| 274 | `@mikan (chipstar182)` | 23 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [mikan_(chipstar182)](https://danbooru.donmai.us/artists/77145) |
| 275 | `@yukizawa xueze` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [yukizawa_xueze](https://danbooru.donmai.us/artists/204181) |
| 276 | `@kodamari` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [kodamari](https://danbooru.donmai.us/artists/31001) |
| 277 | `@rednian` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | low | not_found |
| 278 | `@bellhenge` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [bellhenge](https://danbooru.donmai.us/artists/118982) |
| 279 | `@rezodwel` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [rezodwel](https://danbooru.donmai.us/artists/169014) |
| 280 | `@mebaru` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [mebaru](https://danbooru.donmai.us/artists/105863) |
| 281 | `@liren44` | 23 | ±6 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [liren44](https://danbooru.donmai.us/artists/203815) |
| 282 | `@epic armageddon` | 23 | ±4 | 幻想/暗调倾向、厚涂或概念感 | 暗黑奇幻、氛围角色、概念图 | medium | [epic_armageddon](https://danbooru.donmai.us/artists/126779) |
| 283 | `@usoneko` | 23 | ±6 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [usoneko](https://danbooru.donmai.us/artists/9579) |
| 284 | `@yxyyxy` | 23 | ±6 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [yxyyxy](https://danbooru.donmai.us/artists/110076) |
| 285 | `@overlord jc` | 23 | ±6 | 幻想/暗调倾向、厚涂或概念感 | 暗黑奇幻、氛围角色、概念图 | medium | [overlord_jc](https://danbooru.donmai.us/artists/52092) |
| 286 | `@borgbutler` | 23 | ±4 | 幻想/暗调倾向、厚涂或概念感 | 暗黑奇幻、氛围角色、概念图 | medium | [borgbutler](https://danbooru.donmai.us/artists/284989) |
| 287 | `@boris (noborhys)` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [boris_(noborhys)](https://danbooru.donmai.us/artists/99650) |
| 288 | `@rokuwata tomoe` | 23 | ±6 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [rokuwata_tomoe](https://danbooru.donmai.us/artists/7568) |
| 289 | `@fre (haochilanzuo)` | 23 | ±5 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [fre_(haochilanzuo)](https://danbooru.donmai.us/artists/98482) |
| 290 | `@chuunioniika` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [chuunioniika](https://danbooru.donmai.us/artists/176150) |
| 291 | `@boppin` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [boppin](https://danbooru.donmai.us/artists/204126) |
| 292 | `@ametaro (ixxxzu)` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [ametaro_(ixxxzu)](https://danbooru.donmai.us/artists/292463) |
| 293 | `@heirou` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [heirou](https://danbooru.donmai.us/artists/56951) |
| 294 | `@aka ume` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [aka_ume](https://danbooru.donmai.us/artists/4534) |
| 295 | `@munakata (sekimizu kazuki)` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [munakata_(sekimizu_kazuki)](https://danbooru.donmai.us/artists/99118) |
| 296 | `@nijihashi sora` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [nijihashi_sora](https://danbooru.donmai.us/artists/84087) |
| 297 | `@kakaon` | 23 | ±6 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [kakaon](https://danbooru.donmai.us/artists/155947) |
| 298 | `@ebibi chiriri` | 23 | ±4 | 萌系日系、圆润可爱、明亮柔和 | 萌系少女、头像、日常、小清新 | medium | [ebibi_chiriri](https://danbooru.donmai.us/artists/231184) |
| 299 | `@unacchi (nyusankin)` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [unacchi_(nyusankin)](https://danbooru.donmai.us/artists/57719) |
| 300 | `@sido (slipknot)` | 23 | ±4 | 日系/二次元角色向，具体风格待核实 | 需结合样图二次筛选后使用 | medium | [sido_(slipknot)](https://danbooru.donmai.us/artists/51346) |

## 待复核条目

这些条目未在 Danbooru artist API 中稳定匹配。除非用户点名，优先选择同类中已匹配的 high/medium 画师。

- rank 19: `@toucailao` - 高完成度日系角色、清晰线稿、稳定上色 / 默认泛用、角色立绘、头像、同人插画
- rank 30: `@inaeda kei` - 高完成度日系角色、清晰线稿、稳定上色 / 默认泛用、角色立绘、头像、同人插画
- rank 31: `@inu totemo` - 高完成度日系角色、清晰线稿、稳定上色 / 默认泛用、角色立绘、头像、同人插画
- rank 50: `@die (die0118)` - 高完成度日系角色、清晰线稿、稳定上色 / 默认泛用、角色立绘、头像、同人插画
- rank 55: `@reki (user rcrd4534)` - 高完成度日系角色、清晰线稿、稳定上色 / 默认泛用、角色立绘、头像、同人插画
- rank 76: `@bai qi-qsr` - 华语圈日系插画、细腻上色、角色向 / 少女、古风/幻想、头像、角色立绘
- rank 119: `@mameeekueya` - 萌系日系、圆润可爱、明亮柔和 / 萌系少女、头像、日常、小清新
- rank 159: `@yqgkg` - 日系角色插画、柔和上色、二次元人物向 / 角色参考、头像、轻插画
- rank 214: `@miyabi urumi` - 日系/二次元角色向，具体风格待核实 / 需结合样图二次筛选后使用
- rank 218: `@qian wu atai` - 华语圈日系插画、细腻上色、角色向 / 少女、古风/幻想、头像、角色立绘
- rank 244: `@fangxiang cuoluan` - 华语圈日系插画、细腻上色、角色向 / 少女、古风/幻想、头像、角色立绘
- rank 268: `@kuziaaizuk` - 日系/二次元角色向，具体风格待核实 / 需结合样图二次筛选后使用
- rank 277: `@rednian` - 日系/二次元角色向，具体风格待核实 / 需结合样图二次筛选后使用
