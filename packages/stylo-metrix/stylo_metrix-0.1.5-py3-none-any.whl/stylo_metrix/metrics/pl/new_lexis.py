from ...structures import Metric, Category
from ...utils import ratio

vulgarisms = ['chuj', 'chuja', 'chujek', 'chuju', 'chujem', 'chujnia', 'chujowy', 'chujowa', 'chujowe', 'cipa', 'cipę', 'cipe', 'cipą', 'cipie', 'dojebać', 'dojebac', 'dojebie', 'dojebał', 'dojebal', 'dojebała', 'dojebala', 'dojebałem', 'dojebalem', 'dojebałam', 'dojebalam', 'dojebię', 'dojebie', 'dopieprzać', 'dopieprzac', 'dopierdalać', 'dopierdalac', 'dopierdala', 'dopierdalał', 'dopierdalal', 'dopierdalała', 'dopierdalala', 'dopierdoli', 'dopierdolił', 'dopierdolil', 'dopierdolę', 'dopierdole', 'dopierdoli', 'dopierdalający', 'dopierdalajacy', 'dopierdolić', 'dopierdolic', 'dupa', 'dupie', 'dupą', 'dupcia', 'dupeczka', 'dupy', 'dupe', 'huj', 'hujek', 'hujnia', 'huja', 'huje', 'hujem', 'huju', 'jebać', 'jebac', 'jebał', 'jebal', 'jebie', 'jebią', 'jebia', 'jebak', 'jebaka', 'jebal', 'jebał', 'jebany', 'jebane', 'jebanka', 'jebanko', 'jebankiem', 'jebanymi', 'jebana', 'jebanym', 'jebanej', 'jebaną', 'jebana', 'jebani', 'jebanych', 'jebanymi', 'jebcie', 'jebiący', 'jebiacy', 'jebiąca', 'jebiaca', 'jebiącego', 'jebiacego', 'jebiącej', 'jebiacej', 'jebia', 'jebią', 'jebie', 'jebię', 'jebliwy', 'jebnąć', 'jebnac', 'jebnąc', 'jebnać', 'jebnął', 'jebnal', 'jebną', 'jebna', 'jebnęła', 'jebnela', 'jebnie', 'jebnij', 'jebut', 'koorwa', 'kórwa', 'kurestwo', 'kurew', 'kurewski', 'kurewska', 'kurewskiej', 'kurewską', 'kurewska', 'kurewsko', 'kurewstwo', 'kurwa', 'kurwaa', 'kurwami', 'kurwą', 'kurwe', 'kurwę', 'kurwie', 'kurwiska', 'kurwo', 'kurwy', 'kurwach', 'kurwami', 'kurewski', 'kurwiarz', 'kurwiący', 'kurwica', 'kurwić', 'kurwic', 'kurwidołek', 'kurwik', 'kurwiki', 'kurwiszcze', 'kurwiszon', 'kurwiszona', 'kurwiszonem', 'kurwiszony', 'kutas', 'kutasa', 'kutasie', 'kutasem', 'kutasy', 'kutasów', 'kutasow', 'kutasach', 'kutasami', 'matkojebca', 'matkojebcy', 'matkojebcą', 'matkojebca', 'matkojebcami', 'matkojebcach', 'nabarłożyć', 'najebać', 'najebac', 'najebał', 'najebal', 'najebała', 'najebala', 'najebane', 'najebany', 'najebaną', 'najebana', 'najebie', 'najebią', 'najebia', 'naopierdalać', 'naopierdalac', 'naopierdalał', 'naopierdalal', 'naopierdalała', 'naopierdalala', 'naopierdalała', 'napierdalać', 'napierdala', 'napierdalac', 'napierdalający', 'napierdalajacy', 'napierdolić', 'napierdolic', 'nawpierdalać', 'nawpierdalac', 'nawpierdalał', 'nawpierdalal', 'nawpierdalała', 'nawpierdalala', 'obsrywać', 'obsrywac', 'obsrywający', 'obsrywajacy', 'odpieprzać', 'odpieprzac', 'odpieprzy', 'odpieprzył', 'odpieprzyl', 'odpieprzyła', 'odpieprzyla', 'odpierdalać', 'odpierdalac', 'odpierdol', 'odpierdolił', 'odpierdolil', 'odpierdoliła', 'odpierdolila', 'odpierdoli', 'odpierdalający', 'odpierdalajacy', 'odpierdalająca', 'odpierdalajaca', 'odpierdolić', 'odpierdolic', 'odpierdoli', 'odpierdala', 'odpierdolił', 'opieprzający', 'opierdalać', 'opierdalac', 'opierdala', 'opierdalający', 'opierdalajacy', 'opierdol', 'opierdolić', 'opierdolic', 'opierdoli', 'opierdolą', 'opierdola', 'piczka', 'pieprznięty', 'pieprzniety', 'pieprzony', 'pierdel', 'pierdlu', 'pierdolą', 'pierdola', 'pierdolący', 'pierdolacy', 'pierdoląca', 'pierdolaca', 'pierdol', 'pierdole', 'pierdolenie', 'pierdoleniem', 'pierdoleniu', 'pierdolę', 'pierdolec', 'pierdola', 'pierdolą', 'pierdolić', 'pierdolicie', 'pierdolic', 'pierdolił', 'pierdolil', 'pierdoliła', 'pierdolila', 'pierdoli', 'pierdolnięty', 'pierdolniety', 'pierdolisz', 'pierdolnąć', 'pierdolnac', 'pierdolnął', 'pierdolnal', 'pierdolnęła', 'pierdolnela', 'pierdolnie', 'pierdolnięty', 'pierdolnij', 'pierdolnik', 'pierdolona', 'pierdolone', 'pierdolony', 'pierdołki', 'pierdzący', 'pierdzieć', 'pierdziec', 'pizda', 'pizdą', 'pizde', 'pizdę', 'piździe', 'pizdzie', 'pizdnąć', 'pizdnac', 'pizdu', 'podpierdalać', 'podpierdalac', 'podpierdala', 'podpierdalający', 'podpierdalajacy', 'podpierdolić', 'podpierdolic', 'podpierdoli', 'pojeb', 'pojeba', 'pojebami', 'pojebani', 'pojebanego', 'pojebanemu', 'pojebani', 'pojebany', 'pojebanych', 'pojebanym', 'pojebanymi', 'pojebem', 'pojebać', 'pojebac', 'pojebalo', 'popierdala', 'popierdalac', 'popierdalać', 'popierdolić', 'popierdolic', 'popierdoli', 'popierdolonego', 'popierdolonemu', 'popierdolonym', 'popierdolone', 'popierdoleni', 'popierdolony', 'porozpierdalać', 'porozpierdala', 'porozpierdalac', 'poruchac', 'poruchać', 'przejebać', 'przejebane', 'przejebac', 'przyjebali', 'przepierdalać', 'przepierdalac', 'przepierdala', 'przepierdalający', 'przepierdalajacy', 'przepierdalająca', 'przepierdalajaca', 'przepierdolić', 'przepierdolic', 'przyjebać', 'przyjebac', 'przyjebie', 'przyjebała', 'przyjebala', 'przyjebał', 'przyjebal', 'przypieprzać', 'przypieprzac', 'przypieprzający', 'przypieprzajacy', 'przypieprzająca', 'przypieprzajaca', 'przypierdalać', 'przypierdalac', 'przypierdala', 'przypierdoli', 'przypierdalający', 'przypierdalajacy', 'przypierdolić', 'przypierdolic', 'qrwa', 'rozjebać', 'rozjebac', 'rozjebie', 'rozjebała', 'rozjebią', 'rozpierdalać', 'rozpierdalac', 'rozpierdala', 'rozpierdolić', 'rozpierdolic', 'rozpierdole', 'rozpierdoli', 'rozpierducha', 'skurwić', 'skurwiel', 'skurwiela', 'skurwielem', 'skurwielu', 'skurwysyn', 'skurwysynów', 'skurwysynow', 'skurwysyna', 'skurwysynem', 'skurwysynu', 'skurwysyny', 'skurwysyński', 'skurwysynski', 'skurwysyństwo', 'skurwysynstwo', 'spieprzać', 'spieprzac', 'spieprza', 'spieprzaj', 'spieprzajcie', 'spieprzają', 'spieprzaja', 'spieprzający', 'spieprzajacy', 'spieprzająca', 'spieprzajaca', 'spierdalać', 'spierdalac', 'spierdala', 'spierdalał', 'spierdalała', 'spierdalal', 'spierdalalcie', 'spierdalala', 'spierdalający', 'spierdalajacy', 'spierdolić', 'spierdolic', 'spierdoli', 'spierdoliła', 'spierdoliło', 'spierdolą', 'spierdola', 'srać', 'srac', 'srający', 'srajacy', 'srając', 'srajac', 'sraj', 'sukinsyn', 'sukinsyny', 'sukinsynom', 'sukinsynowi', 'sukinsynów', 'sukinsynow', 'śmierdziel', 'udupić', 'ujebać', 'ujebac', 'ujebał', 'ujebal', 'ujebana', 'ujebany', 'ujebie', 'ujebała', 'ujebala', 'upierdalać', 'upierdalac', 'upierdala', 'upierdoli', 'upierdolić', 'upierdolic', 'upierdoli', 'upierdolą', 'upierdola', 'upierdoleni', 'wjebać', 'wjebac', 'wjebie', 'wjebią', 'wjebia', 'wjebiemy', 'wjebiecie', 'wkurwiać', 'wkurwiac', 'wkurwi', 'wkurwia', 'wkurwiał', 'wkurwial', 'wkurwiający', 'wkurwiajacy', 'wkurwiająca', 'wkurwiajaca', 'wkurwić', 'wkurwic', 'wkurwi', 'wkurwiacie', 'wkurwiają', 'wkurwiali', 'wkurwią', 'wkurwia', 'wkurwimy', 'wkurwicie', 'wkurwiacie', 'wkurwić', 'wkurwic', 'wkurwia', 'wpierdalać', 'wpierdalac', 'wpierdalający', 'wpierdalajacy', 'wpierdol', 'wpierdolić', 'wpierdolic', 'wpizdu', 'wyjebać', 'wyjebac', 'wyjebali', 'wyjebał', 'wyjebac', 'wyjebała', 'wyjebały', 'wyjebie', 'wyjebią', 'wyjebia', 'wyjebiesz', 'wyjebie', 'wyjebiecie', 'wyjebiemy', 'wypieprzać', 'wypieprzac', 'wypieprza', 'wypieprzał', 'wypieprzal', 'wypieprzała', 'wypieprzala', 'wypieprzy', 'wypieprzyła', 'wypieprzyla', 'wypieprzył', 'wypieprzyl', 'wypierdal', 'wypierdalać', 'wypierdalac', 'wypierdala', 'wypierdalaj', 'wypierdalał', 'wypierdalal', 'wypierdalała', 'wypierdalala', 'wypierdalać', 'wypierdolić', 'wypierdolic', 'wypierdoli', 'wypierdolimy', 'wypierdolicie', 'wypierdolą', 'wypierdola', 'wypierdolili', 'wypierdolił', 'wypierdolil', 'wypierdoliła', 'wypierdolila', 'zajebać', 'zajebac', 'zajebie', 'zajebią', 'zajebia', 'zajebiał', 'zajebial', 'zajebała', 'zajebiala', 'zajebali', 'zajebana', 'zajebani', 'zajebane', 'zajebany', 'zajebanych', 'zajebanym', 'zajebanymi', 'zajebiste', 'zajebisty', 'zajebistych', 'zajebista', 'zajebistym', 'zajebistymi', 'zajebiście', 'zajebiscie', 'zapieprzyć', 'zapieprzyc', 'zapieprzy', 'zapieprzył', 'zapieprzyl', 'zapieprzyła', 'zapieprzyla', 'zapieprzą', 'zapieprza', 'zapieprzy', 'zapieprzymy', 'zapieprzycie', 'zapieprzysz', 'zapierdala', 'zapierdalać', 'zapierdalac', 'zapierdalaja', 'zapierdalał', 'zapierdalaj', 'zapierdalajcie', 'zapierdalała', 'zapierdalala', 'zapierdalali', 'zapierdalający', 'zapierdalajacy', 'zapierdolić', 'zapierdolic', 'zapierdoli', 'zapierdolił', 'zapierdolil', 'zapierdoliła', 'zapierdolila', 'zapierdolą', 'zapierdola', 'zapierniczać', 'zapierniczający', 'zasrać', 'zasranym', 'zasrywać', 'zasrywający', 'zesrywać', 'zesrywający', 'zjebać', 'zjebac', 'zjebał', 'zjebal', 'zjebała', 'zjebala', 'zjebana', 'zjebią', 'zjebali', 'zjeby']
intensifiers = ['hiper', 'super', 'mega', 'turbo', 'giga', 'ekstra', 'extra', 'ultra']
exceptions = ['ekstradować', 'ekstradycja', 'ekstradycyjnie', 'ekstradycyjny', 'ekstrahować', 'ekstrakcja', 'ekstrakcyjnie', 'ekstrakcyjny', 'ekstraklasa', 'ekstraklasowiec', 'ekstrakt', 'ekstraktacja', 'ekstraordynaryjnie', 'ekstraordynaryjny', 'ekstraktownia', 'ekstrawagancja', 'ekstrawagancki', 'ekstrawagancko', 'ekstrawaganckość', 'ekstrawersja', 'ekstrawertycznie', 'ekstrawertyczny', 'ekstrawertyk', 'ekstrawertywny', 'ekstrawertyzm', 'gigabajt', 'gigant', 'gigantomachia', 'gigantoman', 'gigantomanka', 'gigantomania', 'gigantyczny', 'gigantyzm', 'hiperaktywny', 'hiperbaryczny', 'hiperbola', 'hiperbolicznie', 'hiperboliczny', 'hiperglikemia', 'hiperinflacja', 'hiperkrytycyzm', 'hiperkrytycznie', 'hiperkrytyczny', 'hiperkrytyka', 'hiperlink', 'hiperlinka', 'hiperłącze', 'hipermarket', 'hipermarketowy', 'hipermarketyzacja', 'hiperonim', 'hiperonimiczny', 'hiperpoprawnie', 'hiperpoprawność', 'hiperpoprawny', 'hipertekst', 'hipertekstowo', 'hipertekstowość', 'hipertekstowy', 'hipertekstualnie', 'hipertekstualność', 'hipertekstualny', 'hipertermia', 'hipertermiczny', 'hipertonia', 'hipertoniczny', 'hipertrofia', 'hipertroficzny', 'hiperwątkowość', 'hiperwątkowy', 'hiperwitaminoza', 'megabajt', 'megabit', 'megabitowy', 'megafon', 'megaherc', 'megalit', 'megalityczny', 'megaloman', 'megalomania', 'megalomanka', 'megalomański', 'megalomańsko', 'megalomaństwo', 'megalopolis', 'megan', 'megapolia', 'megasam', 'megatona', 'megawat', 'megawolt', 'superata', 'supermarket', 'supermarketoza', 'supernowa', 'superowo', 'superowość', 'superowy', 'turbodoładowanie', 'turbować', 'ultradźwięk', 'ultradźwiękowy', 'ultrafiolet', 'ultrafioletowy', 'ultramaryna', 'ultrasonograf', 'ultrasonografia', 'ultrasonograficzny'] 
errors = ['napewno', 'dzień dzisiejszy', 'dniu dzisiejszym', 'dnia dzisiejszego', 'dniem dzisiejszym', 'na prawdę', 'wogóle', 'wogule', 'narazie', 'po za tym', 'pozatym', 'na codzień', 'nacodzień', 'niewiem', 'conajmniej', 'wziąść', 'muj', 'na przeciwko', 'na przeciw', 'jusz', 'ktury', 'z przed', 'zprzed', 'dopuki', 'do póki', 'do puki', 'złodzieji', 'spowrotem', 'żądzić', 'apropo', 'a propo', 'trwać nadal', 'nota bene', 'orginalny', 'nie nawidze', 'nie nawidzę', 'nie nawidzisz', 'nie nawidzi', 'nie nawidza', 'nie nawidzą', 'bende', 'pod rząd', 'nonstop', 'non-stop', 'rzaden', 'okres czasu', 'półtora godziny', 'dlatego bo', 'alkochol', 'muzg', 'puźniej', 'puźno', 'pieniendze', 'piniondze', 'komętarz', 'komętasz', 'kartka papieru', 'krutki', 'krutko', 'przedewszystkim', 'conieco', 'co nie co', 'na wzajem', 'cuż', 'cusz', 'ludzią', 'żygać', 'dzienkuję', 'dzienki', 'z poza', 'nienajlepszy', 'jaki kolwiek', 'jaka kolwiek', 'co kolwiek', 'terz', 'doktór', 'doktur', 'durzy', 'durza', 'durzo', 'misz masz', 'z tąd', 'coniemiara', 'co nie miara', 'w śród', 'chumor', 'pierszy', 'piersza', 'invitro', 'z tamtąd', 'dziecią', 'nisz', 'karzdy', 'dźwi', 'dżwi', 'twuj', 'świerzy', 'kupywać', 'bochater', 'w każdym bądź razie', 'szczelać', 'sczelać', 'lubiałem', 'lubiałam', 'wiencej', 'abstrachując', 'chajs', 'derektor', 'dla czemu', 'fakt autentyczny', 'ogulnie', 'uwarzac', 'pomuż', 'pomusz', 'z pośród', 'po lewo', 'po prawo', 'półtorej roku', 'dlatego ponieważ', 'w gurę', 'akwen wodny', 'wieczur', 'mienso', 'gdzie kolwiek', 'pożądek', 'poszłem', 'mażenia', 'ja rozumie', 'picca', 'przezemnie', 'prze ze mnie', 'nadwyraz', 'urzywać', 'karnister', 'włanczam', 'szczeże', 'swuj', 'przedemną', 'w cudzysłowiu', 'udeżać', 'czym kolwiek', 'przekonywujący', 'charować', 'weszłem', 'spadać w dół', 'wyłanczać', 'wyłanczam', 'kościuł', 'powarzny', 'zdjencie', 'wuzek', 'kszta', 'nastempny', 'po najmniejszej linii oporu', 'brzytki', 'brzytka brzytko', 'serji', 'porzyczka', 'do czekać', 'jak kolwiek', 'przenica', 'ksiondz', 'swetr', 'wyszłem', 'umię', 'perfuma', 'bezemnie', 'cofać do tyłu', 'filmuw', 'samochud', 'wzięłem', 'poniewarz', 'ubrać kurtkę', 'ubrać sukienkę', 'z na przeciwka', 'znaprzeciwka', 'coprawda', 'języczek uwagi', 'wudka', 'prze piękny', 'półtorej tygodnia', 'konfort', 'ważywa', 'naczczo', 'nadczo', 'naogó', 'na ogul', 'supskrybować', 'bez wypadkowy', 'tendy', 'wdodatku', 'w woli ścisłości', 'tamtendy', 'zmenczenie', 'kawałek torta', 'wciąż kontynuuje', 'naniby', 'wizawi', 'obkoło', 'na obkoło', 'którendy', 'umią', 'przyjacielami'] 
adv_phrases = ['a battuta', 'a capella', 'a cappella', 'a conto', 'a fronte', 'a limine', 'a posteriori', 'a priori', 'à rebours', 'a rebours', 'ab initio', 'ab intra', 'ab urbe condita', 'ad acta', 'ad hoc', 'ad infinitum', 'ad mortem defecatam', 'al fine', 'allegro assai', 'allegro con brio', 'allegro con moto', 'allegro maestoso', 'allegro moderato', 'allegro, ma non troppo', 'ani na jotę', 'ani trochę', 'ante meridiem', 'au rebours', 'bądź co bądź', 'bez cienia wątpliwości', 'bez dwóch zdań', 'bez głowy', 'bez jaj', 'bez kitu', 'bez krępacji', 'bez ładu i składu', 'bez obsłonek', 'bez ogródek', 'bez osłonek', 'bez owijania w bawełnę', 'bez oznak życia', 'bez pamięci', 'bez pardonu', 'bez pochyby', 'bez porównania', 'bez pośpiechu', 'bez przerwy', 'bez przestanku', 'bez sensu', 'bez serca', 'bez wątpienia', 'bez wytchnienia', 'bez zarzutu', 'bez życia', 'bladym świtem', 'byle jak', 'cały czas', 'całymi dniami', 'chcąc nie chcąc', 'cicho jak w grobie', 'cicho niczym w grobie', 'ciemno jak w dupie u Murzyna', 'ciemno, choć w pysk daj', 'co chwila', 'co chwilę', 'co dnia', 'co do joty', 'co do zasady', 'co dopiero', 'co dzień', 'co miesiąc', 'co najwyżej', 'co roku', 'co sił w nogach', 'co tchu', 'co wieczór', 'con anima', 'często-gęsto', 'dawno i nieprawda', 'dawno, dawno temu', 'dawnymi czasy', 'de facto', 'de iure', 'dla beki', 'dla świętego spokoju', 'do chrzanu', 'do cna', 'do dupy', 'do góry', 'do góry nogami', 'do greckich kalend', 'do grobowej deski', 'do imentu', 'do kitu', 'do ostatniego tchu', 'do ostatniej kropli krwi', 'do potęgi', 'do przodu', 'do rzici', 'do szaleństwa', 'do szczęta', 'do szczętu', 'do szpiku kości', 'do tego', 'do tej pory', 'do tyłu', 'do usranego końca', 'do usranej śmierci', 'do wyboru, do koloru', 'do zmroku', 'do żywego', 'dokoła Wojtek', 'dookoła Wojtek', 'dopiero co', 'dwa kroki', 'dwa kroki stąd', 'dzień po dniu', 'en bloc', 'en détail', 'en face', 'ex aequo', 'ex situ', 'fa presto', 'fair play', 'forte fortissimo', 'fortissimo possibile', 'ganc pomada', 'gdzie indziej', 'gdzie pieprz rośnie', 'gołym okiem', 'gołymi rękami', 'grosso modo', 'i tak dalej', 'ianuis clausis', 'ile fabryka dała', 'ile sił', 'in extenso', 'in flagranti', 'in minus', 'in plus', 'in situ', 'in statu nascendi', 'in suspenso', 'in vitro', 'in vivo', 'inter alia', 'jak amen w pacierzu', 'jak Bóg przykazał', 'jak by nie patrzeć', 'jak cholera', 'jak cię mogę', 'jak diabli', 'jak groch przy drodze', 'jak groch przy drodze, kto idzie, to go głodze', 'jak grochem o ścianę', 'jak grom z jasnego nieba', 'jak jeden mąż', 'jak kot z pęcherzem', 'jak krew w piach', 'jak Pan Bóg stworzył', 'jak po szynach', 'jak rak świśnie a ryba piśnie', 'jak się patrzy', 'jak skurwysyn', 'jak słoń w składzie porcelany', 'jak ta lala', 'jak u Pana Boga za piecem', 'jak w chińskim banku', 'jak w dym', 'jak w szwajcarskim banku', 'jak z bicza trzasł', 'jak znalazł', 'jak żółw', 'jakby chciał, a nie mógł', 'jakimś cudem', 'jeden za drugim', 'jednym słowem', 'jeszcze raz', 'kawa na ławę', 'każdego dnia', 'każdego roku', 'kiedy indziej', 'kilka razy', 'koniec końców', 'krok po kroku', 'kropka w kropkę', 'ku czci', 'ku przestrodze', 'kubek w kubek', 'lata świetlne temu', 'łeb w łeb', 'lege artis', 'lelum polelum', 'lepiej nie mówić', 'lotem błyskawicy', 'między innymi', 'między młotem a kowadłem', 'MM', 'moim zdaniem', 'na abarot', 'na amen', 'na amyn', 'na antenie', 'na backę', 'na bakier', 'na bank', 'na barana', 'na bieżąco', 'na blachę', 'na bogato', 'na boku', 'na całej linii', 'na chłopczycę', 'na chybił trafił', 'na cito', 'na ćmiywku', 'na co dzień', 'na cołki łeb', 'na czas', 'na czczo', 'na czele', 'na czerwono', 'na czwartej', 'na dobę', 'na dobitkę', 'na dobrą sprawę', 'na dobre i na złe', 'na dobrej stopie', 'na dodatek', 'na dole', 'na domiar złego', 'na drodze', 'na drugiej', 'na dużym ekranie', 'na dworze', 'na dwunastej', 'na dzień', 'na dziesiątej', 'na dziewiątej', 'na fajka', 'na falach eteru', 'na fest', 'na gapę', 'na garnuszku', 'na gębę', 'na glanc', 'na głodniaka', 'na głos', 'na głowę', 'na golasa', 'na gorąco', 'na gorącym uczynku', 'na górze', 'na haju', 'na hura', 'na jedenastej', 'na jednej nodze', 'na jedno kopyto', 'na jeża', 'na kacu', 'na koń', 'na końcu świata', 'na koszt firmy', 'na krzywy ryj', 'na krzyż', 'na ładne oczy', 'na łapu-capu', 'na łeb na szyję', 'na lewą stronę', 'na lewo', 'na luzie', 'na małpę', 'na małym ekranie', 'na miejscu', 'na mocy', 'na mokro', 'na mur', 'na nowo', 'na odpieprz', 'na odpierdol', 'na odpierdziel', 'na odwal', 'na ogół', 'na oko', 'na oścież', 'na ósmej', 'na ostatnich nogach', 'na pamięć', 'na patataj', 'na pęczki', 'na pewniaka', 'na pewno', 'na piątej', 'na pierwszej', 'na piśmie', 'na pniu', 'na początku', 'na podwójnym gazie', 'na pokaz', 'na pół', 'na pół gwizdka', 'na poły', 'na potęgę', 'na pował', 'na powietrzu', 'na pozoryndziu', 'na prask', 'na priv', 'na próbę', 'na próżno', 'na przekór', 'na przemian', 'na przestrzeni wieków', 'na raz', 'na razie', 'na równi', 'na rybkę', 'na rympał', 'na rzadko', 'na serio', 'na setkę', 'na siedząco', 'na siłę', 'na siódmej', 'na skraju', 'na spokojnie', 'na sposób', 'na stałe', 'na sto dwa', 'na sto procent', 'na stojąco', 'na stronie', 'na styk', 'na sucho', 'na surowo', 'na świętego Dygdy', 'na święty nigdy', 'na swój sposób', 'na szagę', 'na szaro', 'na szczęście', 'na szóstej', 'na temat', 'na ten raz', 'na topie', 'na trzeciej', 'na ucho', 'na ukos', 'na ustęp', 'na waleta', 'na wieczne czasy', 'na wieczór', 'na wieki', 'na wieki wieków', 'na wiosnę', 'na własną rękę', 'na własne oczy', 'na wolnym ogniu', 'na wpół', 'na wskroś', 'na wszelki wypadek', 'na wyciągnięcie ręki', 'na wynos', 'na wznak', 'na zamówienie', 'na zasadzie', 'na zawsze', 'na zewnątrz', 'na zimno', 'na złamanie karku', 'na zmianę', 'na żywca', 'na żywo', 'nad wyraz', 'nade wszystko', 'nawiasem mówiąc', 'ni chuja', 'ni mniej, ni więcej', 'ni w ząb', 'ni z gruszki, ni z pietruszki', 'nic a nic', 'nie bardzo', 'nie bez kozery', 'nie da się ukryć', 'nie do końca', 'nie do wiary', 'nie do wytrzymania', 'nie kijem, to pałką', 'nie ma mowy', 'nie na miejscu', 'nie po drodze', 'nie tak', 'nie za bardzo', 'nigdy indziej', 'nigdy w świecie', 'nigdzie indziej', 'noga za nogą', 'nomen omen', 'non stop', 'o brzasku', 'o chlebie i wodzie', 'o czasie', 'o dwa kroki stąd', 'o majland', 'o mało', 'o mało co', 'o mały włos', 'o poranku', 'o rzut kamieniem', 'o suchym pysku', 'o świcie', 'o świtaniu', 'o wiele', 'o wschodzie', 'o zmierzchu', 'o zmroku', 'od a do zet', 'od czapy', 'od czasu do czasu', 'od czubka głowy do pięt', 'od dawna', 'od deski do deski', 'od dupy strony', 'od dziecka', 'od jakiegoś czasu', 'od kołyski', 'od kołyski do grobu', 'od małego', 'od maleńkości', 'od niedawna', 'od nowa', 'od przedwojny', 'od razu', 'od ręki', 'od stóp do głów', 'od tylca', 'od wielkiego dzwonu', 'od zarania', 'od zarania dziejów', 'od zawsze', 'od… do…', 'ode złego amyn', 'opere citato', 'ostatni raz', 'ostatnimi czasy', 'pa duszam', 'par excellence', 'pełną gębą', 'per analogiam', 'per nogam', 'per rectum', 'pi razy drzwi', 'pi razy oko', 'pic rel', 'piździ jak w Kieleckiem', 'plus minus', 'po angielsku', 'po arabsku', 'po białorusku', 'po birmańsku', 'po bratersku', 'po chińsku', 'po Chrystusie', 'po chuju', 'po cichu', 'po ciemku', 'po cieszyńsku', 'po ćmi', 'po ćmoku', 'po części', 'po daleku', 'po darmu', 'po darymnicy', 'po dobroci', 'po drodze', 'po dziś dzień', 'po dzisiejszemu', 'po estońsku', 'po florencku', 'po francusku', 'po grecku', 'po grób', 'po harapie', 'po hebrajsku', 'po hiszpańsku', 'po japońsku', 'po katolicku', 'po kaznodziejsku', 'po kobiecemu', 'po kolei', 'po koreańsku', 'po krakowsku', 'po królewsku', 'po kryjomu', 'po kumotersku', 'po łacinie', 'po łacińsku', 'po litewsku', 'po łotewsku', 'po ludzku', 'po macku', 'po macoszemu', 'po męsku', 'po mistrzowsku', 'po mojemu', 'po nitce do kłębka', 'po nocy', 'po omacku', 'po partnersku', 'po pierwsze', 'po pijaku', 'po pijanemu', 'po polskiemu', 'po polsku', 'po południu', 'po portugalsku', 'po prawej', 'po prostu', 'po próżnicy', 'po sąsiedzku', 'po śląsku', 'po swojemu', 'po szwedzku', 'po turecku', 'po ukraińsku', 'po uszy', 'po węgiersku', 'po wiedeńsku', 'po wieki', 'po wieki wieków', 'po włosku', 'po wsze czasy', 'po wszystkie czasy', 'po zadku', 'po zmroku', 'pod gazem', 'pod gołym niebem', 'pod koniec', 'pod nosem', 'pod publiczkę', 'pod wieczór', 'pod wodą', 'pod wpływem', 'post meridiem', 'post mortem', 'prędzej czy później', 'primo voto', 'pro anno', 'prosto w nos', 'prosto w oczy', 'prosto z mostu', 'przed Chrystusem', 'przed laty', 'przede wszystkim', 'przy drzwiach zamkniętych', 'przy kości', 'przy okazji', 'psim swędem', 'rada w radę', 'ramię w ramię', 'raz na jakiś czas', 'raz na ruski rok', 'raz na sto lat', 'raz po raz', 'rękami i nogami', 'rok po roku', 'rok w rok', 'ruski miesiąc', 'rzut beretem', 'sam na sam', 'secundo voto', 'siłą rzeczy', 'skoro świt', 'sobie a muzom', 'spode łba', 'średnio na jeża', 'tak czy siak', 'tak na dobrą sprawę', 'tak samo', 'tak sobie', 'tam, gdzie król chodzi piechotą', 'tam, gdzie król piechotą chodzi', 'tego lata', 'tempo di ballo', 'tertio voto', 'toutes proportions gardées', 'trzy cztery', 'tu i ówdzie', 'tu i tam', 'twarzą w twarz', 'tym razem', 'u dołu', 'u góry', 'u spodu', 'una corda', 'va banque', 'vice versa', 'w afekcie', 'w biały dzień', 'w bród', 'w ciągu dnia', 'w ciąży', 'w czas', 'w czasach słusznie minionych', 'w cztery oczy', 'w czwórnasób', 'w dechę', 'w dobie', 'w dodatku', 'w dół', 'w drobną kaszkę', 'w drobny mak', 'w dupie', 'w dwóch słowach', 'w dwójnasób', 'w dyrdy', 'w dzień', 'w głąb', 'w głównej mierze', 'w górę', 'w grudniu po południu', 'w istocie', 'w kółko', 'w koło Macieju', 'w końcu', 'w krótkich abcugach', 'w kucki', 'w lansadach', 'w lewo', 'w majestacie prawa', 'w mgnieniu oka', 'w miarę', 'w mig', 'w moich oczach', 'w najlepsze', 'w nieskończoność', 'w nocy', 'w obliczu śmierci', 'w oddali', 'w ogóle', 'w okamgnieniu', 'w ostateczności', 'w pełni', 'w pizdu', 'w pobliżu', 'w pocie czoła', 'w poprzek', 'w porę', 'w porząsiu', 'w przód', 'w przybliżeniu', 'w ramionach Morfeusza', 'w rumel', 'w rzeczywistości', 'w sam czas', 'w siną dal', 'w skrócie', 'w ślimaczym tempie', 'w sosie własnym', 'w sposób', 'w środku', 'w stroju Adama', 'w stroju adamowym', 'w stroju Ewy', 'w sumie', 'w swoim czasie', 'w szczególności', 'w tę i we w tę', 'w te pędy', 'w trakcie', 'w try miga', 'w trymiga', 'w tym', 'w ujęciu', 'w ukryciu', 'w założeniu', 'w zamian', 'w zasięgu ręki', 'w żółwim tempie', 'we dwójnasób', 'wesoło jak w rodzinnym grobie', 'własną piersią', 'wsio rawno', 'wszem wobec', 'wszerz i wzdłuż', 'wszystko jedno', 'wte i wewte', 'wzdłuż i wszerz', 'z automatu', 'z biglem', 'z całego serca', 'z cicha', 'z czasem', 'z dala', 'z daleka', 'z dnia na dzień', 'z dokładnością do', 'z duszą na ramieniu', 'z dystansu', 'z dziada pradziada', 'z głupia frant', 'z górki na pazurki', 'z góry', 'z grubej rury', 'z grubsza', 'z kąta w kąt', 'z klasą', 'z klejnotami na wierzchu', 'z kolei', 'z krakowska', 'z kretesem', 'z łatwością', 'z lotu ptaka', 'z marszu', 'z miejsca', 'z miesiąca na miesiąc', 'z miłą chęcią', 'z nastaniem nocy', 'z oddali', 'z osobna', 'z otwartymi ramionami', 'z pewnością', 'z pocałowaniem ręki', 'z podniesionym czołem', 'z pompą', 'z pośpiechem', 'z powrotem', 'z prądem', 'z premedytacją', 'z przodu', 'z przymrużeniem oka', 'z rąsi', 'z reguły', 'z ręką na sercu', 'z ręki', 'z roku na rok', 'z rozsądku', 'z rzadka', 'z tarczą lub na tarczy', 'z tygodnia na tydzień', 'z tyłu', 'z ukosa', 'z ukrycia', 'z uporem maniaka', 'z wiatrem', 'z wieczora', 'z wierzchu', 'z wolna', 'z żabiej perspektywy', 'z założenia', 'z zamkniętymi oczami', 'z zasady', 'z zimną krwią', 'za bezcen', 'za Bóg zapłać', 'za chińskiego boga', 'za Chiny', 'za Chiny ludowe', 'za chuja', 'za czasem', 'za darmo', 'za darmochę', 'za dnia', 'za facke', 'za frajer', 'za friko', 'za granicą', 'za grosze', 'za każdym razem', 'za kółkiem', 'za miskę soczewicy', 'za młodu', 'za nastawnikiem', 'za nic', 'za nic na świecie', 'za nic w świecie', 'za pięć dwunasta', 'za pobraniem', 'za pół ceny', 'za skarby świata', 'za wszelką cenę', 'za żadną cenę', 'za żadne pieniądze', 'za żadne skarby', 'za żadne skarby świata', 'za zamkniętymi drzwiami', 'ze słuchu', 'ze smakiem', 'ze szczętem', 'zimno jak w psiarni', 'żółwim krokiem'] 
adv_temp = ['dziś', 'dzisiaj', 'wczoraj', 'przedwczoraj', 'jutro', 'pojutrze', 'teraz', 'obecnie', 'ostatnio', 'dawno', 'dawniej', 'wcześniej', 'później', 'niebawem', 'zaraz', 'aktualnie', 'rano', 'wieczorem']
adv_dur = ['stale', 'ciągle', 'wciąż', 'cały czas', 'nieustannie', 'nieprzerwanie', 'bez przerwy', 'permanentnie', 'bezustannie', 'bez ustanku', 'nieustająco', 'non stop']
adv_freq = ['rzadko', 'rzadziej', 'często', 'częściej', 'najczęściej', 'z rzadka', 'nierzadko', 'nieczęsto', 'czasem', 'czasami', 'epizodycznie', 'wielokrotnie', 'parokrotnie', 'parę razy', 'kilka razy', 'kilkukrotnie', 'po wielekroć', 'po wielokroć']

class Leksyka(Category):
  lang='pl'
  name_en='Lexis'
  name_local='Leksyka'
		
class L_NAME(Metric):
    category = Leksyka
    name_en = "Proper names"
    name_local = "Nazwy wlasne"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'PROPN']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_NAME_M(Metric):
    category = Leksyka
    name_en = "Masculine proper nouns"
    name_local = "Nazwy wlasne w rodzaju meskim"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == "PROPN"
        and str(token.morph.get('Gender')) == "['Masc']"]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_NAME_F(Metric):
    category = Leksyka
    name_en = "Feminine proper nouns"
    name_local = "Nazwy wlasne w rodzaju zenskim"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == "PROPN"
        and str(token.morph.get('Gender')) == "['Fem']"]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_NAME_ENT(Metric):
    category = Leksyka
    name_en = "Named entities"
    name_local = "Jednostki nazewnicze"

    def count(doc):
        debug = [token.text for token in doc if token.ent_type_ != '']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_PLACEN_GEOG(Metric):
    category = Leksyka
    name_en = "Place and geographical names"
    name_local = "Nazwy miejsc i nazwy geograficzne"

    def count(doc):
        debug = [token.text for token in doc if token.ent_type_ in ['PLACENAME', 'GEOGNAME']
                and str(token.morph.get('Animacy'))!='[\'Hum\']'
                and str(token.morph.get('Animacy'))!='[\'Inan\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_PERSN(Metric):
    category = Leksyka
    name_en = "Person names"
    name_local = "Nazwy osob"

    def count(doc):
        debug = [token.text for token in doc if token.ent_type_ == 'PERSNAME']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_ORGN(Metric):
    category = Leksyka
    name_en = "Organization names"
    name_local = "Nazwy organizacji"

    def count(doc):
        debug = [token.text for token in doc if token.ent_type_ == 'ORGNAME']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_ETHN(Metric):
    category = Leksyka
    name_en = "Ethnonyms and demonyms"
    name_local = "Etnonimy i demonimy"

    def count(doc):
        debug = [token.text for token in doc if token.ent_type_ in ['GEOGNAME', 'PLACENAME']
                 and str(token.morph.get('Animacy'))=='[\'Hum\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_GEOG_ADJ(Metric):
    category = Leksyka
    name_en = "Adjectives derived from geographical names"
    name_local = "Przymiotniki wywodzące się od nazw geograficznych"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ == 'ADJ'
                and token.ent_type_ in ['GEOGNAME', 'PLACENAME']
                and str(token.morph.get('Animacy'))=='[\'Inan\']']
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_DATE(Metric):
    category = Leksyka
    name_en = "Dates"
    name_local = "Daty"

    def count(doc):
        debug = [token.text for token in doc if token.ent_type_ == 'DATE']
        result = len(debug)
        return ratio(result, len(doc)), debug

class L_VULG(Metric):
    category = Leksyka
    name_en = "Vulgarisms"
    name_local = "Wulgaryzmy"

    def count(doc):
        debug = [token.text.lower() for token in doc if token.text.lower() in vulgarisms]
        result = len(debug)
        return ratio(result, len(doc)), debug

class L_INTENSIF(Metric):
    category = Leksyka
    name_en = "Degree modifiers of Greek origin"
    name_local = "Modyfikatory natężenia cechy pochodzenia greckiego"

    def count(doc):
        debug = [token.text for token in doc if token.lemma_.lower() in intensifiers
        or any(prefix for prefix in intensifiers if token.text.lower().startswith(prefix))
        and not token.lemma_ in exceptions]
        result = len(debug)
        return ratio(result, len(doc)), debug
    
class L_ERROR(Metric):
    category = Leksyka
    name_en = "Common linguistic errors"
    name_local = "Czeste bledy jezykowe"

    def count(doc):
        words = [token.text.lower() for token in doc]
        debug = []
        total_matched_words = 0
        current_phrase = []

        sorted_phrases = sorted(errors, key=lambda x: len(x.split()), reverse=True)

        for entry in sorted_phrases:
            entry = entry.lower()
            if " " in entry:
                phrase_tokens = entry.split()
                if entry in doc.text.lower():
                    if all(token in doc.text.lower() for token in phrase_tokens):
                        is_contained = any(phrase in debug for phrase in phrase_tokens)
                        if not is_contained:
                            is_partial_contained = any(phrase in " ".join(debug) for phrase in phrase_tokens)
                            if not is_partial_contained:
                                debug.append(" ".join(phrase_tokens))
                                total_matched_words += len(phrase_tokens)
            elif entry in words:
                debug.append(entry)
                total_matched_words += 1

        return ratio(total_matched_words, len(words)), debug
    
class L_ADVPHR(Metric):
    category = Leksyka
    name_en = "Adverbial phrases"
    name_local = "Frazy przyslowkowe"

    def count(doc):
        words = [token.text.lower() for token in doc]
        debug = []
        total_matched_words = 0
        current_phrase = []

        sorted_phrases = sorted(adv_phrases, key=lambda x: len(x.split()), reverse=True)

        for entry in sorted_phrases:
            entry = entry.lower()
            if " " in entry:
                phrase_tokens = entry.split()
                if entry in doc.text.lower():
                    if all(token in doc.text.lower() for token in phrase_tokens):
                        is_contained = any(phrase in debug for phrase in phrase_tokens)
                        if not is_contained:
                            is_partial_contained = any(phrase in " ".join(debug) for phrase in phrase_tokens)
                            if not is_partial_contained:
                                debug.append(" ".join(phrase_tokens))
                                total_matched_words += len(phrase_tokens)
            elif entry in words:
                debug.append(entry)
                total_matched_words += 1

        return ratio(total_matched_words, len(words)), debug
    
class L_ADV_TEMP(Metric):
    category = Leksyka
    name_en = "Adverbs of time"
    name_local = "Przyslowki temporalne"

    def count(doc):
        words = [token.text.lower() for token in doc]
        debug = []
        total_matched_words = 0
        current_phrase = []

        for entry in adv_temp:
            entry = entry.lower()
            if " " in entry:
                phrase_tokens = entry.split()
                if entry in doc.text.lower():
                    debug.append(" ".join(phrase_tokens))
                    total_matched_words += len(phrase_tokens)
            elif entry in words:
                debug.append(entry)
                total_matched_words += 1

        return ratio(total_matched_words, len(words)), debug
		
class L_ADV_DUR(Metric):
    category = Leksyka
    name_en = "Adverbs of duration"
    name_local = "Przyslowki duratywne"

    def count(doc):
        words = [token.text.lower() for token in doc]
        debug = []
        total_matched_words = 0
        current_phrase = []

        for entry in adv_dur:
            entry = entry.lower()
            if " " in entry:
                phrase_tokens = entry.split()
                if entry in doc.text.lower():
                    debug.append(" ".join(phrase_tokens))
                    total_matched_words += len(phrase_tokens)
            elif entry in words:
                debug.append(entry)
                total_matched_words += 1

        return ratio(total_matched_words, len(words)), debug
		
class L_ADV_FREQ(Metric):
    category = Leksyka
    name_en = "Adverbs of frequency"
    name_local = "Przyslowki czestotliwosci"

    def count(doc):
        words = [token.text.lower() for token in doc]
        debug = []
        total_matched_words = 0
        current_phrase = []

        for entry in adv_freq:
            entry = entry.lower()
            if " " in entry:
                phrase_tokens = entry.split()
                if entry in doc.text.lower():
                    debug.append(" ".join(phrase_tokens))
                    total_matched_words += len(phrase_tokens)
            elif entry in words:
                debug.append(entry)
                total_matched_words += 1

        return ratio(total_matched_words, len(words)), debug
		
class L_SYL_G1(Metric):
    category = Leksyka
    name_en = "One-syllable words"
    name_local = "Wyrazy jednosylabowe"

    def count(doc):
        debug = [token.text for token in doc if token._.syllables_count is not None and token._.syllables_count == 1]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_SYL_G2(Metric):
    category = Leksyka
    name_en = "Two-syllables words"
    name_local = "Wyrazy dwusylabowe"

    def count(doc):
        debug = [token.text for token in doc if token._.syllables_count is not None and token._.syllables_count == 2]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_SYL_G3(Metric):
    category = Leksyka
    name_en = "Three-syllables words"
    name_local = "Wyrazy trojsylabowe"

    def count(doc):
        debug = [token.text for token in doc if token._.syllables_count is not None and token._.syllables_count == 3]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_SYL_G4(Metric):
    category = Leksyka
    name_en = "Words formed of 4 or more syllables"
    name_local = "Wyrazy o liczbie sylab wiekszej niż 3"

    def count(doc):
        debug = [token.text for token in doc if token._.syllables_count is not None and token._.syllables_count > 3]
        result = len(debug)
        return ratio(result, len(doc)), debug
	
class L_TTR_IA(Metric):
    category = Leksyka
    name_en = "Type-token ratio for non-lemmatized tokens"
    name_local = "Type-token ratio dla wyrazów w odmianach"

    def count(doc):

        results = set([token.text.lower() for token in doc if token.is_punct == False])
        debug = {'FOUND': results}
        return ratio(len(results), len(doc)), debug
		
class L_TTR_LA(Metric):
    category = Leksyka
    name_en = "Type-token ratio for lemmatized tokens"
    name_local = "Type-token ratio dla wyrazów zlematyzowanych"

    def count(doc):

        results = set([token.lemma_.lower() for token in doc if token.is_punct == False])
        debug = {'FOUND': results}
        return ratio(len(results), len(doc)), debug
		
class L_CONT_A(Metric):
    category = Leksyka
    name_en = "Incidence of content words"
    name_local = "Wyrazy samodzielne"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ not in ["PART", "SYM", "ADP", "X", "DET", "CCONJ", "SCONJ", "PUNCT", "INTJ"]]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_CONT_T(Metric):
    category = Leksyka
    name_en = "Content words types"
    name_local = "Typy wyrazow samodzielnych"

    def count(doc):
        debug = set(token.text for token in doc if token.pos_ not in ["PART", "SYM", "ADP", "X", "DET", "CCONJ", "SCONJ", "PUNCT", "INTJ"])
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_CONT_L(Metric):
    category = Leksyka
    name_en = "Content words lemma types"
    name_local = "Typy lemm wyrazow samodzielnych"

    def count(doc):
        debug = set(token.lemma_ for token in doc if token.pos_ not in ["PART", "SYM", "ADP", "X", "DET", "CCONJ", "SCONJ", "PUNCT", "INTJ"])
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_FUNC_A(Metric):
    category = Leksyka
    name_en = "Incidence of function words"
    name_local = "Slowa funkcyjne"

    def count(doc):
        debug = [token.text for token in doc if token.pos_ in ["PART", "ADP", "DET", "CCONJ", "SCONJ"]]
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_FUNC_T(Metric):
    category = Leksyka
    name_en = "Function words types"
    name_local = "Typy wyrazow funkcyjnych"

    def count(doc):
        debug = set(token.text for token in doc if token.pos_ in ["PART", "ADP", "DET", "CCONJ", "SCONJ"])
        result = len(debug)
        return ratio(result, len(doc)), debug
		
class L_FUNC_L(Metric):
    category = Leksyka
    name_en = "Function words lemma types"
    name_local = "Typy lemm wyrazow funkcyjnych"

    def count(doc):
        debug = set(token.lemma_ for token in doc if token.pos_ in ["PART", "ADP", "DET", "CCONJ", "SCONJ"])
        result = len(debug)
        return ratio(result, len(doc)), debug