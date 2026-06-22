#!/usr/bin/env python3.11
# Segment JA i18n strings with BudouX (preserving HTML tags), inject ZWSP,
# then rewrite the `const I18N = {...}` block in index.html in place.
# 2026-06-21 rev2: plain / easy-to-read Japanese (GINPEI: 難しい表現が多すぎる).
import re, pathlib, budoux

ZWSP = "​"
p = budoux.load_default_japanese_parser()

DICT = {
  'tg':'音を聴いた瞬間に、景色が見える',
  'cover.bl':'アートディレクション・ガイド ／ ムードボード',
  'adg':'アートディレクション・ガイド',

  'p2.title':'目次',
  'p2.brk':'［ 目次 ］',
  'p2.disclaim':'このガイドは、dreamtape のすべての制作物の見た目の方向を決める。',
  'toc.03':'ブランドの人格とアーキタイプ','toc.03h':'チャート',
  'toc.04':'ビジュアルの柱','toc.04h':'一覧',
  'toc.05':'ムードボード I ― シネマティックな街','toc.05h':'暖かい',
  'toc.06':'ムードボード II ― 気配','toc.06h':'影',
  'toc.07':'ムードボード III ― 夢の風景','toc.07h':'広い',
  'toc.08':'ムードボード IV ― アナログと質感','toc.08h':'質感',
  'toc.09':'モーション ― 映像のスタイル','toc.09h':'フィルム',
  'toc.10':'タイポグラフィ ― 二つの声','toc.10h':'書体',
  'toc.11':'書体の使い方','toc.11h':'使い方',
  'toc.12':'カラー','toc.12h':'パレット',
  'toc.13':'リリース・スリーブ','toc.13h':'スリーブ',
  'toc.apx':'アノマリー ― 検討中のアイデア','toc.apxh':'未確定',
  'toc.ref':'実写トーンの参照 ― 実在の写真','toc.refh':'×2',

  'ref.brk':'［ 参照のみ ］',
  'ref.r':'私たちの画像ではない',
  'ref.note':'ブランド全体で使うトーンと質感 ― 最終画像ではない。',
  'refw.title':'実写リファレンス',
  'refw.l':'実在の写真 ・ 全テーマ',
  'refw.h':'私たちのではない ―<br>合わせにいく感じ',
  'refw.p1':'<b>これは私たちの画像ではない。</b>集めてきた参照用の写真で、dreamtape が合わせにいく実在のトーン。',
  'refw.p2':'CGではなくフィルム。ふちが温かく、少し褪せていて、作り込まない。光が仕事をして、人は半分隠れたまま。まずこの感じ ― 粒子、夕暮れ、静けさ ― を合わせる。dreamtape の一枚を作る前に。',
  'ref.disclaim':'実在の写真の参照 ― めざす<b>トーンと質感</b>。最終画像ではない。',
  'ref.adg':'実写トーン参照 ・ 二人の間で',
  'ref1.title':'実写 ― 夢の風景と光','ref1.l':'実在の写真 ・ トーンと光',
  'ref2.title':'実写 ― アナログと粒状','ref2.l':'実在の写真 ・ テープと粒状',
  'ref3.title':'実写 ― 気配と色','ref3.l':'実在の写真 ・ 人影と色',
  'ref4.title':'実写 ― 静かな上質','ref4.l':'実在の写真 ・ 抑制された上質',

  'p3.title':'ブランドの人格とアーキタイプ',
  'p3.brk':'［ どんなブランドか ］',
  'p3.kmag':'■ マジシャン 80%','p3.keve':'■ エヴリマン 20%',
  'p3.h3':'マジシャン、でも目線は同じ。',
  'p3.p1':'<b>マジシャン（80%）。</b>dreamtape は世界をつくり、その中に入っていける。種明かしはしない。作品が映画で、音楽はそのサウンドトラック。風景を見せて、そこに留まるかは聴く人にまかせる。',
  'p3.p2':'<b>エヴリマン（20%）。</b>二人の作り手は、聴く人の上ではなく隣に立つ。演じない、ありのままの声。高級そうに見せることも、煽ることもしない。',
  'p3.p3':'約束は、静かで確かなもの。<em>夢を見られなくなった人に、もう一度夢を届ける。</em>',
  'p3.disclaim':'制作はこの決まりから<b>外れない</b>こと。',

  'p4.title':'ビジュアルの柱',
  'p4.brk':'［ ビジュアルのテーマ ］','p4.r':'6つの要素',
  'p4.t1':'シネマティック・ヴィンテージ','p4.d1':'映画のセットのような夕暮れの街。横長の画で、霞んで、沈んでいく。',
  'p4.t2':'感覚としてのテープ','p4.d2':'カセットそのものではなく、そこに残る温度。ヒスノイズ、粒子、色あせたフィルムのにじみ。',
  'p4.t3':'ヴィンテージ・オーガニック・ドライ','p4.d3':'デジタルよりアナログ。ほこり、粒子、陽に焼けた色。つやは出さない。',
  'p4.t4':'夢の風景（ドリームスケープ）','p4.d4':'その音を聴いた瞬間に浮かぶ風景。',
  'p4.t5':'溶けていく気配','p4.d5':'作り手は見せず、感じさせる。光に溶けていく人の影。',
  'p4.t6':'ウォーム × マシン','p4.d6':'冷たく精密なマシンが、温かい夢を包む。dreamtape らしさをつくる組み合わせ。',

  'p5.title':'ムードボード I ― シネマティックな街','p5.l':'暖かい ・ 街 ・ ゴールデンアワー','p5.brk':'［ 夕暮れの街 ］',
  'p6.title':'ムードボード II ― 気配','p6.l':'影 ・ 逆光 ・ 顔を見せない','p6.brk':'［ 見せず、感じさせる ］','p6.note':'顔は出さない。逆光と影だけ。',
  'p7.title':'ムードボード III ― 夢の風景','p7.l':'広い ・ パステル ・ 人がいない','p7.brk':'［ 音から生まれる風景 ］','p7.r':'地平線','p7.hero':'DR.01 · SALT FLATS ― 聴いた瞬間、風景が浮かぶ',
  'p8.title':'ムードボード IV ― アナログと質感','p8.l':'手ざわり ・ ざらつき ・ ドライ','p8.brk':'［ CGではなく、録ったもの ］','p8.r':'素材サンプル',
  'p9.title':'モーション ― 映像のスタイル','p9.brk':'［ ビジュアライザーは短編映画 ］','p9.r':'その瞬間に',

  'p10.title':'タイポグラフィ ― 二つの声','p10.r':'書体 ・ 2ファミリー',
  'p10.role1':'<span class="accent">ディスプレイ</span>',
  'p10.lab1':'Bebas Neue ・ 1ウェイト<br>見出し ・ 大きなキーワード',
  'p10.role2':'実用の声',
  'p10.lab2':'Helvetica Neue<br>Bold ・ Medium ・ Regular<br>ワードマーク ・ 本文 ・ ラベル',
  'p10.disclaim':'Bebas は見出し、Helvetica は文章。<b>声は二つ、それだけ。</b>',

  'p11.title':'書体の使い方','p11.l':'階層 ・ 組み合わせ ・ 使い方','p11.brk':'［ 二つの声を重ねる ］',
  'p11.k1':'キーワード<br>Bebas','p11.k2':'見出し<br>Bebas','p11.k3':'ワードマーク<br>Helv 700','p11.k4':'サブ見出し<br>Helv 500 斜体','p11.k5':'本文<br>Helv 400','p11.k6':'キャプション<br>Helv 500',
  'p11.note':'<b>Bebas は見出し用</b> ― すべての見出しとキーワードに。<b>Helvetica は文章用</b> ― ワードマーク、本文、ラベル、すべての表記に。アクセントは一色 ― <span class="accent">テラコッタ</span> ― それだけ。',

  'p12.title':'カラー','p12.l':'暖かい夢 × 冷たいマシン','p12.brk':'［ アクセントは一色だけ ］','p12.r':'7色',
  'c.ink':'インク','c.inku':'文字・基本',
  'c.steel':'スチール','c.steelu':'マシン・メタデータ',
  'c.acc':'アクセント','c.terra':'テラコッタ','c.terrau':'唯一のアクセント',
  'c.amber':'アンバー','c.amberu':'ゴールデンアワー',
  'c.sand':'サンド','c.sandu':'アナログの色',
  'c.sage':'セージ','c.sageu':'色あせた地平',
  'c.paper':'ペーパー','c.paperu':'下地',
  'p12.note':'冷たい色をベースに、温かいアクセントを一つ。はっきりした色は<b>テラコッタ</b>だけで、あとは落ち着いた色。',

  'p13.title':'リリース・スリーブ','p13.brk':'［ ひとつの画面に、すべて ］',
  'p13.h3':'すべてが成り立つ証明。',
  'p13.p':'アナログの粒子を通した夢の風景 ― Bebas のキーワードを一語、Helvetica Bold のワードマーク、Helvetica のクレジット、テラコッタのアクセントを一つ。温かい夢と冷たいマシン、ひとつの世界。',
  'p13.c1':'夢の風景','p13.c2':'アナログ粒子','p13.c5':'スチール × テラコッタ',

  'apx.title':'付録 ― アノマリー','apx.l':'ギャップ探し ・ 検討中','apx.brk':'［ ガイドには含めない ］','apx.r':'二人の監督へ',
  'apx.note':'夢の中に、美しい侵入者をひとつ ― 別の世界から来た物体。決定ではなく、意見をもらうためのスケッチ。',
  'apx.hero':'AX.01 · MONOLITH ― 温かい夢の中にぽつんとある、光のもとが見えない精密な物体',
  'apx.disclaim':'探索だけ ― <b>方向ではない</b>。確定したものはない。二人で形にしていく。',
  'apx.adg':'アイデア ・ ガイドではない'
}

TAG = re.compile(r'<[^>]+>')
# 2字熟語などBudouXが語中分割しがちな保護語(ZWSPを内側から除去)
PROTECT = ['方向','世界','機構','構造','風景','温度','粒子','景色','物体','精密','監督',
           '検討','探索','逆光','気配','質感','階層','人格','正体','都市','地平','制作',
           '緊張','侵入','感覚','記録','映画','音楽','作品','瞬間','地平線','種明かし']

def seg(text):
    if not re.search(r'[぀-ヿ一-鿿]', text):
        return text
    return ZWSP.join(p.parse(text))

def segment_html(s):
    out, last = [], 0
    for m in TAG.finditer(s):
        out.append(seg(s[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(seg(s[last:]))
    return ''.join(out)

lines = ['const I18N = {']
keys = list(DICT.keys())
for i, k in enumerate(keys):
    v = segment_html(DICT[k])
    for w in PROTECT:                      # 保護語の語中ZWSPを除去(語中分割を防ぐ)
        v = v.replace(ZWSP.join(list(w)), w)
    if "'" in v or "\\" in v:
        v = v.replace("\\", "\\\\").replace("'", "\\'")
    comma = ',' if i < len(keys)-1 else ''
    lines.append(f"  '{k}':'{v}'{comma}")
lines.append('}')
literal = '\n'.join(lines)

path = str(pathlib.Path(__file__).resolve().parent.parent / 'index.html')
html = open(path, encoding='utf-8').read()
new, n = re.subn(r'const I18N = \{.*?\n\}', literal, html, count=1, flags=re.DOTALL)
assert n == 1, f"replacement count={n}"
open(path, 'w', encoding='utf-8').write(new)
print(f"OK replaced I18N block ({len(keys)} keys). ZWSP count in file:", new.count(ZWSP))
