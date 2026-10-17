# تشخيص الفهرسة — 17 شتنبر 2026

## ما الذي يثبته ملف Search Console؟

آخر يوم في `Chart.csv` هو 14 شتنبر 2026: صفحتان مفهرستان و5 روابط مستبعدة. ويسجل الملف 173 ظهوراً في البحث بين 19 يونيو و14 شتنبر 2026؛ الظهور لا يعني زيارة. التصدير لا يحتوي على عناوين هذه الصفحات، ولا بيانات النقرات أو الزيارات أو التثبيتات.

| السبب في التقرير | العدد | المعنى والخطوة اللازمة |
| --- | --- | --- |
| Not found (404) | 1 | الصورة اللاحقة من Search Console حددت الرابط: `https://floatboard.xyz/download`. أُضيف إصلاح محلي لتحويله إلى قسم التحميل، ويحتاج النشر قبل إعادة التحقق. |
| Page with redirect | 3 | الرابط المحوّل نفسه لا يحتاج إلى الفهرسة؛ افحص وجهته النهائية إذا كانت صفحة مهمة. |
| Alternate page with proper canonical tag | 1 | نسخة بديلة لها رابط أساسي؛ استبعادها ليس دليلاً على منع فهرسة الموقع. |

هذه الحالات موضحة في [وثائق Google لتقرير الفهرسة](https://support.google.com/webmasters/answer/7440203). لا يمكن تحديد هوية الصفحتين المفهرستين أو رابط 404 من هذا التصدير وحده.

## تحديد رابط 404 وإصلاحه

الصورة التي أُرسلت بعد الفحص حددت `https://floatboard.xyz/download`، وآخر زحف ظاهر له كان 26 غشت 2026. الفحص المباشر أكد أن `/download` و`/download/` يعيدان 404 قبل النشر. قسم التحميل الموجود فعلياً هو `https://floatboard.xyz/#download`، وكان نموذج واجهة الحافظة في الرئيسية يعرض المسار القديم كنص.

أُضيف `download/index.html` حتى يصبح مسار التحميل القديم موجوداً على الاستضافة الثابتة. يعيد المتصفح توجيه الزائر فوراً إلى `/#download` باستخدام `meta refresh` بمدة صفر، ويعمل ذلك حتى مع تعطيل JavaScript. ويوجد رابط ظاهر بديل إلى التحميل. الملف يحدد الرئيسية كـ canonical، ولا يُضاف مسار التحويل إلى sitemap. كما صُحح الرابط المعروض في نموذج واجهة الحافظة.

هذا تحويل داخل HTML وليس إعداد HTTP 301 إلى الرئيسية. Google يعتبر `meta refresh` الفوري إشارة تحويل دائم عندما يتعذر ضبط التحويل على الخادم؛ [مرجع Google للتحويلات](https://developers.google.com/search/docs/crawling-indexing/301-redirects). بعد النشر قد يظهر الرابط ضمن Page with redirect بدلاً من Not found، وهو متوقع؛ المطلوب فهرسة الوجهة الأساسية.

## نتيجة فحص الموقع المنشور قبل التعديل

- الرئيسية و`pricing.html` و`privacy.html` و`terms.html` و`refund.html` استجابت بـ HTTP 200.
- `robots.txt` يسمح بالزحف، ويشير إلى `https://floatboard.xyz/sitemap.xml`، وملف sitemap متاح ويُقرأ كـ XML.
- لم يظهر حظر `noindex` على الصفحات الخمس المفحوصة.
- نسختا HTTP وwww من الرئيسية تحولان إلى `https://floatboard.xyz/`.
- `/index.html` يستجيب بـ 200 ويشير بالـ canonical إلى `/`. استبعاد نسخة كهذه طبيعي؛ لا دليل في ZIP على أنها النسخة المذكورة تحديداً.
- استجابة مسار غير موجود كانت 404 فعلية. لم تتم إضافة تحويل شامل إلى الرئيسية لأنه لا يعالج سبب الرابط المفقود.
- الاستضافة المنشورة تظهر `Server: GitHub.com`. إضافة إعدادات تحويل خاصة بـ Vercel إلى هذا المستودع لا تصلح إعدادات GitHub Pages تلقائياً.

وقت الفحص، سجل [GitHub API للإصدار v1.0.15](https://api.github.com/repos/nazihyazan/floating_board/releases/tags/v1.0.15) مجموع **94 عملية تنزيل** لملفات الإصدار: 31 EXE، و7 AppX، و23 macOS ZIP، و23 DEB، و7 RPM، و3 AppImage. هذه عدادات تنزيل ملفات وليست عدد مستخدمين فريدين أو تثبيتات مؤكدة، ويمكن أن تشمل تنزيلات آلية أو مكررة.

## التعديلات المنفذة

- تحسين عنوان الرئيسية ووصفها وH1 والمحتوى الظاهر حول floating notes وalways-on-top notes وclipboard manager وclipboard history وcopy and paste.
- إضافة `floating-notes.html` لشرح استعمال الملاحظات أثناء الكتابة والبحث، و`clipboard-manager.html` لشرح تجميع المراجع وإعادة استخدام النصوص المنسوخة. لكل صفحة عنوان ووصف ورابط أساسي مستقل، وروابط من الرئيسية وإليها.
- إكمال sitemap ليشمل الصفحات السبع الأساسية، بما فيها سياسة الاسترجاع. تواريخ `lastmod` تعكس تعديل الصفحات في 17 شتنبر 2026. لا تغيّر التاريخ تلقائياً عند كل نشر؛ غيّره عند تحديث فعلي للمحتوى أو الروابط أو البيانات المنظمة. حُذفت `priority` لأن Google يتجاهلها، وفق [وثائق sitemap](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).
- توحيد روابط العودة للرئيسية على `/` بدل `/index.html`، مع الحفاظ على عناوين `.html` الحالية للصفحات الأخرى.
- تصحيح روابط الأيقونة والمشاركة لتستخدم `/icon.png` الموجود في المستودع؛ المسار `/assets/icon.png` كان غير موجود محلياً، لكنه استجاب بـ 200 على الموقع المنشور وقت الفحص. لذلك لا ننسب إليه خطأ 404 الموجود في Search Console.
- تحسين وصف التطبيق في بيانات `SoftwareApplication` المنظمة بما يتفق مع المحتوى، دون إضافة تقييمات أو مراجعات غير موجودة.
- إبقاء المحتوى ظاهراً دون الاعتماد على JavaScript، واستعمال عناصر `details/summary` للأسئلة الشائعة، وتحسين التفاف التنقل والأزرار على الهاتف.
- إضافة أوصاف وviewport وروابط تنقل للصفحات القانونية؛ نصوص السياسات لم تتغير.

أُزيلت خانة `meta keywords` لأنها لا تؤثر على فهرسة Google أو ترتيبه؛ الكلمات المستهدفة موجودة في النص المفيد والعناوين والروابط. [مرجع Google](https://developers.google.com/search/docs/crawling-indexing/special-tags).

## التحقق المحلي

- فحص XML وتفرّد روابط sitemap وتطابق كل رابط مع canonical وصفحة موجودة.
- فحص العناوين والأوصاف وH1 والروابط الداخلية والصور وJSON-LD وإمكانية الوصول للصفحات السبع من الرئيسية.
- اختبار الرئيسية والصفحتين الجديدتين في Chromium بعرض 1440 و390 بكسل، مع JavaScript وبدونه: لا موارد محلية مفقودة أو أخطاء JavaScript أو محتوى رئيسي مخفي؛ الأسئلة الشائعة تعمل، وكذلك تغيير المظهر واختيار حزمة Linux عند تشغيل JavaScript.
- اختبار `/download` و`/download/` و`/download/index.html` في Chromium مع JavaScript وبدونه: المسارات الستة المختبرة تصل إلى `/#download` ويظهر زر تحميل Windows. الخادم المحلي يحول `/download` إلى `/download/` ثم يقدم صفحة التحويل بـ 200؛ يجب تأكيد الاستجابة المنشورة بعد النشر.
- الفحص المحلي لا يؤكد فهرسة Google؛ التغييرات تحتاج النشر والزحف إليها أولاً.

## بعد نشر الملفات

1. تأكد أن الرئيسية والصفحتين الجديدتين و`sitemap.xml` المنشورة تحتوي على التعديلات وأن الروابط الأساسية تستجيب بـ 200.
2. في خاصية `floatboard.xyz` داخل Search Console، أرسل `https://floatboard.xyz/sitemap.xml` من Sitemaps.
3. افحص `https://floatboard.xyz/` ثم `https://floatboard.xyz/floating-notes.html` ثم `https://floatboard.xyz/clipboard-manager.html` عبر URL Inspection → Test live URL. راجع الوصول والرابط الأساسي ثم اختر Request indexing إذا كان الاختبار ناجحاً.
4. افتح `https://floatboard.xyz/download` وتأكد أنه يوصلك إلى قسم التحميل. في Search Console افحص نفس الرابط عبر Test live URL، ثم افتح Page indexing → Not found (404) واختر Validate fix بعد نجاح الفحص. لا تطلب فهرسة مسار التحويل نفسه؛ افحص الرئيسية باعتبارها الوجهة الأساسية.
5. تابع Search results → Performance لمعرفة الاستعلامات والظهور والنقرات على الصفحات المهمة. تقرير Coverage وحده لا يقيس الزيارات أو التنزيلات. قارن تنزيلات GitHub خلال فترات محددة بدلاً من افتراض أنها صفر.

طلب إعادة الزحف قد يحتاج أياماً أو أسابيع ولا يضمن الفهرسة؛ تكرار نفس الطلب لا يسرّعه. [إرشادات Google لطلب إعادة الزحف](https://developers.google.com/search/docs/crawling-indexing/ask-google-to-recrawl). تحسين المحتوى والفهرسة لا يضمن المرتبة الأولى.

---

# تحديث وتطوير الفهرسة — 17 أكتوبر 2026

## 1. حل مشكلة تعليق قراءة خريطة الموقع (Couldn't fetch / Type: Unknown)
في فحص Google Search Console لشهر أكتوبر 2026، ظهرت خريطة الموقع `sitemap.xml` بحالة `Couldn't fetch` ونوع `Unknown` مع 0 صفحات مكتشفة، بينما الفحص المباشر (Live URL Test) أظهر أن الرابط يعمل بشكل طبيعي كصفحة عادية (`Crawled - currently not indexed`).

### الأسباب الجذرية والإصلاحات البرمجية:
1. **ترويسات الخادم (HTTP Headers):** أُضيف ملف `_headers` في جذر المشروع لفرض ترويسة `Content-Type: application/xml; charset=utf-8` على Cloudflare Pages، مع ترويسة منع الكاش `Cache-Control: public, max-age=0, must-revalidate` وترويسة `X-Robots-Tag: noindex` لمنع أرشفة الخريطة كصفحة محتوى.
2. **صياغة ملف XML القياسية:** تم توحيد السطر الأول إلى `<?xml version="1.0" encoding="UTF-8"?>` بعلامات تنصيص مزدوجة ودون أي أسطر فارغة أو مسافات سابقة.
3. **كسر كاش Search Console:** تم إنشاء خريطة موقع جديدة باسم `sitemap-main.xml` متطابقة تماماً مع الخريطة الأساسية ومزامنتها برمجياً عبر `scripts/build-blog.py`.
4. **تحديث robots.txt:** أُدرجت الخريطتان معاً في ملف `robots.txt`.

## 2. توسيع استراتيجية الكلمات المفتاحية التجارية (Commercial & Piggyback SEO)
تم إنشاء ونشر 5 صفحات هبوط جديدة مخصصة لاستهداف كلمات شرائية ذات منافسة منخفضة في أسواق الفئة الأولى (Tier-1):
- `/alternatives/pureref-with-text-and-clipboard.html`: بديل PureRef للملاحظات وسجل الحافظة مع الصور.
- `/compare/floatboard-vs-powertoys-always-on-top.html`: مقارنة مع PowerToys Always on Top (بطاقات خفيفة بدل نوافذ كاملة).
- `/alternatives/windows-sticky-notes-always-on-top.html`: حل لمشكلة غياب ميزة التثبيت في Windows Sticky Notes.
- `/alternatives/ditto-copyq-visual-clipboard.html`: بديل مرئي عصري لقوائم Ditto و CopyQ التقليدية.
- `/linux/floating-clipboard-notes-ubuntu.html`: صفحة مخصصة لمستخدمي لينكس وأوبونتو وتثبيت Snapcraft.

## 3. تحويل قراء المدونة إلى مستخدمين ومشترين
- تضمين صناديق دعوة تفاعلية (Callout Boxes) أوتوماتيكياً في مقدمة جميع مقالات المدونة الـ 19 لربطها بصفحات التحميل `/download/` والميزات.
- إضافة روابط فوتر مطابقة للكلمات المفتاحية (Exact-Match Links) في جميع صفحات الموقع.
- تحديث بيانات `SoftwareApplication` (JSON-LD) لتعكس رخصة $5.99 مدى الحياة (Lifetime License).

## 4. التحقق البرمجي النهائي
- تشغيل أداة الفحص `scripts/check-seo.py`: اجتياز جميع الفحوصات بنجاح لـ **34 صفحة معيارية (Canonical Pages)**، وتأكيد تفرّد العناوين والأوصاف، وسلامة جميع الروابط والصور وبيانات Schema.

