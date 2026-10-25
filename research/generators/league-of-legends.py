import json, sys

OUT = "/Users/kaneki/Desktop/workspace/Projects - Scrap/lorelines/research/league-of-legends.json"

WIKI = "https://leagueoflegends.fandom.com/wiki/"
ARCW = "https://arcane.fandom.com/wiki/"
UNIV = "https://universe.leagueoflegends.com/en_US/"

sources = []
def src(key, url, title, publisher):
    sources.append({"key": key, "url": url, "title": title, "publisher": publisher})

# ---------- official Universe ----------
src("u-search", "https://universe-meeps.leagueoflegends.com/v1/en_us/search/index.json", "Universe of League of Legends - search index (champions and factions JSON)", "official")
CHAMPS = {
 "aatrox": "Aatrox", "ahri": "Ahri", "akali": "Akali", "akshan": "Akshan", "ambessa": "Ambessa", "anivia": "Anivia",
 "annie": "Annie", "ashe": "Ashe", "aurelionsol": "Aurelion Sol", "azir": "Azir", "bard": "Bard", "belveth": "Bel'Veth",
 "braum": "Braum", "caitlyn": "Caitlyn", "cassiopeia": "Cassiopeia", "darius": "Darius", "diana": "Diana", "draven": "Draven",
 "ekko": "Ekko", "evelynn": "Evelynn", "ezreal": "Ezreal", "galio": "Galio", "gangplank": "Gangplank", "garen": "Garen",
 "graves": "Graves", "gwen": "Gwen", "hecarim": "Hecarim", "heimerdinger": "Heimerdinger", "illaoi": "Illaoi", "irelia": "Irelia",
 "janna": "Janna", "jarvaniv": "Jarvan IV", "jax": "Jax", "jayce": "Jayce", "jhin": "Jhin", "jinx": "Jinx", "kaisa": "Kai'Sa",
 "kalista": "Kalista", "kassadin": "Kassadin", "katarina": "Katarina", "kayle": "Kayle", "kayn": "Kayn", "leblanc": "LeBlanc",
 "leona": "Leona", "lissandra": "Lissandra", "lucian": "Lucian", "lux": "Lux", "malphite": "Malphite", "malzahar": "Malzahar",
 "mel": "Mel", "missfortune": "Miss Fortune", "mordekaiser": "Mordekaiser", "morgana": "Morgana", "nasus": "Nasus",
 "olaf": "Olaf", "ornn": "Ornn", "pantheon": "Pantheon", "poppy": "Poppy", "pyke": "Pyke", "qiyana": "Qiyana", "rakan": "Rakan",
 "rell": "Rell", "renekton": "Renekton", "riven": "Riven", "ryze": "Ryze", "sejuani": "Sejuani", "senna": "Senna",
 "seraphine": "Seraphine", "shen": "Shen", "shyvana": "Shyvana", "singed": "Singed", "sion": "Sion", "sivir": "Sivir",
 "skarner": "Skarner", "swain": "Swain", "sylas": "Sylas", "syndra": "Syndra", "taliyah": "Taliyah", "thresh": "Thresh",
 "twistedfate": "Twisted Fate", "varus": "Varus", "vayne": "Vayne", "veigar": "Veigar", "velkoz": "Vel'Koz", "vi": "Vi",
 "viego": "Viego", "viktor": "Viktor", "vladimir": "Vladimir", "volibear": "Volibear", "warwick": "Warwick", "xayah": "Xayah",
 "xerath": "Xerath", "xinzhao": "Xin Zhao", "yasuo": "Yasuo", "yone": "Yone", "yorick": "Yorick", "zed": "Zed", "zeri": "Zeri",
 "zilean": "Zilean", "zoe": "Zoe", "lulu": "Lulu",
}
for slug, name in CHAMPS.items():
    src("u-" + slug, UNIV + "story/champion/" + slug + "/", name + " - biography (Universe of League of Legends)", "official")
FACTIONS = {"bandle-city": "Bandle City", "bilgewater": "Bilgewater", "demacia": "Demacia", "freljord": "The Freljord",
            "ionia": "Ionia", "ixtal": "Ixtal", "mount-targon": "Targon", "noxus": "Noxus", "piltover": "Piltover",
            "shadow-isles": "Shadow Isles", "shurima": "Shurima", "void": "The Void", "zaun": "Zaun"}
for slug, name in FACTIONS.items():
    src("u-region-" + slug, UNIV + "region/" + slug + "/", name + " - region overview (Universe of League of Legends)", "official")

# ---------- League of Legends Wiki ----------
W = [
 ("wiki-timeline", "Timeline", "Timeline (Runeterra Prime chronology and calendar)"),
 ("wiki-creation", "Creation_of_the_Universe", "Creation of the Universe"),
 ("wiki-formation", "Formation_of_Runeterra", "Formation of Runeterra"),
 ("wiki-titan-war", "Titan_War", "Titan War"),
 ("wiki-founding-freljord", "Founding_of_the_Freljord", "Founding of the Freljord"),
 ("wiki-three-sisters", "War_of_the_Three_Sisters", "War of the Three Sisters"),
 ("wiki-westward", "Westward_Migration", "Westward Migration"),
 ("wiki-golden-age", "Golden_Age_of_the_Shuriman_Empire", "Golden Age of the Shuriman Empire"),
 ("wiki-void-war", "Void_War", "Void War"),
 ("wiki-fall-shurima", "Fall_of_Shurima", "Fall of Shurima"),
 ("wiki-darkin-war", "Great_Darkin_War", "Great Darkin War"),
 ("wiki-iron-revenant", "Reign_Of_The_Iron_Revenant", "Reign of the Iron Revenant"),
 ("wiki-ruination", "Ruination_of_Helia", "Ruination of Helia"),
 ("wiki-rune-wars", "Rune_Wars", "Rune Wars"),
 ("wiki-resurgence", "Resurgence_of_Civilizations", "Resurgence of Civilizations"),
 ("wiki-first-war", "First_Demacian-Noxian_War", "First Demacian-Noxian War"),
 ("wiki-recent", "Recent_History", "Recent History"),
 ("wiki-invasion", "Noxian_Invasion_of_Ionia", "Noxian Invasion of Ionia"),
 ("wiki-sun-disc", "Rebirth_of_the_Sun_Disc", "Rebirth of the Sun Disc"),
 ("wiki-ruined-king", "Return_of_the_Ruined_King", "Return of the Ruined King"),
 ("wiki-mage-rebellion", "Great_Mage_Rebellion", "Great Mage Rebellion"),
 ("wiki-kda", "Riot_Records/KDA", "Riot Records / K/DA skin universe"),
 ("wiki-star-guardian", "Star_Guardian_(Universe)", "Star Guardian (Universe)"),
 ("wiki-arcane-universe", "Arcane_(Universe)", "Arcane (Universe)"),
 ("wiki-arcane-s1", "Arcane_(TV_Series)/Season_1", "Arcane (TV Series) / Season 1"),
]
for key, page, title in W:
    src(key, WIKI + page, title + " - League of Legends Wiki", "wiki")

# ---------- Arcane Wiki ----------
A = [
 ("arcwiki-s2", "Season_2", "Season 2"),
 ("arcwiki-s1e9", "The_Monster_You_Created", "The Monster You Created (S1E9)"),
 ("arcwiki-s2e1", "Heavy_is_the_Crown", "Heavy is the Crown (S2E1)"),
 ("arcwiki-s2e3", "Finally_Got_the_Name_Right", "Finally Got the Name Right (S2E3)"),
 ("arcwiki-s2e5", "Blisters_and_Bedrock", "Blisters and Bedrock (S2E5)"),
 ("arcwiki-s2e6", "The_Message_Hidden_Within_the_Pattern", "The Message Hidden Within the Pattern (S2E6)"),
 ("arcwiki-s2e7", "Pretend_Like_It%27s_the_First_Time", "Pretend Like It's the First Time (S2E7)"),
 ("arcwiki-s2e8", "Killing_Is_a_Cycle", "Killing Is a Cycle (S2E8)"),
 ("arcwiki-s2e9", "The_Dirt_Under_Your_Nails", "The Dirt Under Your Nails (S2E9)"),
]
for key, page, title in A:
    src(key, ARCW + page, title + " - Arcane Wiki", "wiki")

# ---------- Wikipedia ----------
src("wp-kda", "https://en.wikipedia.org/wiki/K/DA", "K/DA - Wikipedia", "other")
src("wp-popstars", "https://en.wikipedia.org/wiki/Pop/Stars", "Pop/Stars - Wikipedia", "other")
src("wp-allout", "https://en.wikipedia.org/wiki/All_Out_(EP)", "All Out (EP) - Wikipedia", "other")
src("wp-more", "https://en.wikipedia.org/wiki/More_(K/DA_song)", "More (K/DA song) - Wikipedia", "other")
src("wp-arcane", "https://en.wikipedia.org/wiki/Arcane_(TV_series)", "Arcane (TV series) - Wikipedia", "other")

# ======================= TIMELINES =======================
timelines = [
 {"slug": "runeterra", "name": "Runeterra Prime (canon)", "kind": "canon", "parent": None, "branch_note": None,
  "description": "The main League of Legends continuity on the world of Runeterra, dated by the Noxian calendar (BN/AN) and told through the Universe biographies, short stories and events."},
 {"slug": "arcane", "name": "Arcane (TV series)", "kind": "alternate", "parent": "runeterra",
  "branch_note": "Branches from canon Piltover and Zaun history: the show gives Vi and Powder/Jinx, Jayce, Viktor and Silco a new shared backstory (for example, Viktor first meets Jayce after his trial, while canon has them meet at a Progress Day party) and ends with events the game canon does not follow one-to-one.",
  "description": "The Netflix and Fortiche animated series (Season 1 in November 2021, Season 2 in November 2024) about the sisters Vi and Jinx and the conflict between Piltover and Zaun over hextech and shimmer."},
 {"slug": "kda", "name": "K/DA", "kind": "au", "parent": None,
  "branch_note": "A contemporary music skin universe, not a branch of Runeterra history. Riot treats it as a separate setting that it shares with True Damage, Pentakill, HEARTSTEEL and DJ Sona.",
  "description": "A modern-day world where Ahri, Akali, Evelynn and Kai'Sa form the virtual K-pop girl group K/DA, with Seraphine as a guest artist. Its history is told through real-world song and skin releases."},
 {"slug": "star-guardian", "name": "Star Guardian", "kind": "au", "parent": None,
  "branch_note": "A magical-girl skin universe set in Valoran City, not a branch of Runeterra history.",
  "description": "Teens chosen by the First Star protect the universe from Void beasts and fallen guardians. It is told in seasons released in 2016, 2017, 2019 and 2022."},
]

# ======================= ENTITIES =======================
entities = []
def ent(slug, name, kind, summary, sources_, timeline=None, variant_of=None, aliases=None):
    entities.append({"slug": slug, "name": name, "kind": kind, "timeline": timeline, "variant_of": variant_of,
                     "aliases": aliases or [], "summary": summary, "sources": sources_})

# --- places / regions (factions) ---
ent("runeterra", "Runeterra", "place", "The world in which League of Legends is set. Unknown beings shaped it with the World Runes, and it has both a physical realm and a spirit realm.", ["wiki-creation", "wiki-formation"])
ent("demacia", "Demacia", "faction", "A lawful, proud kingdom in western Valoran with a strong military tradition. Refugees from the Rune Wars founded it in petricite forests as a refuge from magic, and it is now in turmoil over its treatment of mages.", ["u-region-demacia", "wiki-rune-wars", "wiki-resurgence"])
ent("noxus", "Noxus", "faction", "An expansionist empire that values strength and lets anyone rise by talent. It grew from Noxii tribes that sheltered in the Immortal Bastion during the Rune Wars, and its founding is year 0 of the calendar.", ["u-region-noxus", "wiki-resurgence"])
ent("ionia", "Ionia", "faction", "An archipelago of allied provinces known as the First Lands, where the border with the spirit realm is thin. The Noxian invasion scarred it, and factions still fight over its future.", ["u-region-ionia", "wiki-invasion"], aliases=["The First Lands"])
ent("freljord", "The Freljord", "faction", "A harsh northern land of proud warrior tribes. Its ancient history turns on the war between the sisters Avarosa, Serylda and Lissandra, and the tribes still fight over that legacy.", ["u-region-freljord", "wiki-three-sisters"])
ent("shurima", "Shurima", "faction", "A desert empire that once spanned a continent, ruled by the Ascended god-warriors. It fell when Azir's Ascension failed, and it is now rising again under the reborn emperor.", ["u-region-shurima", "wiki-fall-shurima", "wiki-sun-disc"])
ent("mount-targon", "Mount Targon", "place", "The tallest peak in Runeterra and a place of pilgrimage. Those who reach its summit can become hosts for the celestial Aspects.", ["u-region-mount-targon", "wiki-westward"], aliases=["Targon"])
ent("piltover", "Piltover", "faction", "A rich, progressive city of trade and invention on cliffs above Zaun. It grew around the Sun Gates and is the birthplace of hextech.", ["u-region-piltover", "wiki-resurgence"], aliases=["City of Progress"])
ent("zaun", "Zaun", "faction", "The undercity district in the canyons below Piltover, full of chemical smog and industry. It began as the old port of Oshra Va'Zaun and partly sank in the 772 AN disaster.", ["u-region-zaun", "wiki-resurgence"], aliases=["Oshra Va'Zaun", "the Undercity"])
ent("bilgewater", "Bilgewater", "faction", "A lawless port city in the Serpent Isles, home to pirates, monster hunters and smugglers. Outsiders settled it with the consent of the Buhru people in 787 AN.", ["u-region-bilgewater", "wiki-resurgence"])
ent("shadow-isles", "Shadow Isles", "place", "Once the Blessed Isles, home of the enlightened city of Helia. The Ruination merged the material and spirit realms there, and the Black Mist now traps the souls of the dead.", ["u-region-shadow-isles", "wiki-ruination"], aliases=["Blessed Isles"])
ent("ixtal", "Ixtal", "faction", "A secluded jungle nation of elemental mages ruled by the Yun Tal from Ixaocan. It survived the Void and the Darkin, and later sealed its borders during the Rune Wars.", ["u-region-ixtal", "wiki-westward", "wiki-rune-wars"])
ent("bandle-city", "Bandle City", "place", "The hidden home of the yordles, reached through paths beyond the material realm. Early yordles founded it around the Bandle Tree in the spirit realm.", ["u-region-bandle-city", "wiki-formation"])
ent("void", "The Void", "faction", "A hungry nothingness from beyond reality, ruled by the Watchers. Its creatures, the Voidborn, try to consume Runeterra.", ["u-region-void", "wiki-creation"])
ent("icathia", "Icathia", "place", "An ancient mage kingdom in southern Shurima. Shurima conquered it, and when it rebelled it opened a Void rift that destroyed the land.", ["wiki-westward", "wiki-golden-age", "wiki-void-war"])
ent("camavor", "Camavor", "place", "A lost kingdom on an eastern continent, ruled by King Viego. It fell into ruin after the Ruination, and the rest of Runeterra forgot it.", ["wiki-ruination", "wiki-rune-wars"])
ent("helia", "Helia", "place", "The city of scholars on the Blessed Isles that guarded dangerous relics and the Waters of Life. The Ruination destroyed it in 25 BN.", ["wiki-ruination", "wiki-westward"])
ent("immortal-bastion", "The Immortal Bastion", "place", "The fortress Mordekaiser built at the center of his empire. The Noxii later sheltered in it during the Rune Wars, and it became the heart of Noxus.", ["wiki-iron-revenant", "wiki-resurgence"])

# --- organizations / factions within ---
ent("ascended", "The Ascended Host", "organization", "God-warriors made by the Shuriman Ascension ritual at the Sun Disc. They ruled Shurima for millennia, and many later became the Darkin.", ["wiki-golden-age", "u-region-shurima"], aliases=["God-Warriors", "Sunborn"])
ent("darkin", "The Darkin", "faction", "Ascended who were twisted by the Void War and the fall of Shurima and turned against the world. The Aspects and mortal mages sealed them into their own weapons.", ["wiki-darkin-war", "u-aatrox"], aliases=["the fallen"])
ent("watchers", "The Watchers", "faction", "Ancient entities of the Void who woke as reality expanded. Lissandra made a pact with them, and they are now entombed in True Ice under the Howling Abyss.", ["wiki-creation", "wiki-founding-freljord", "wiki-three-sisters"])
ent("black-rose", "The Black Rose", "organization", "A secret cabal of mages that steers Noxus from the shadows. It began when LeBlanc and Vladimir met during Mordekaiser's reign.", ["wiki-iron-revenant", "u-leblanc"])
ent("kinkou-order", "The Kinkou Order", "organization", "Ionian warriors who keep the balance between the material and spirit realms. Shen leads them as the Eye of Twilight.", ["u-shen", "wiki-recent"], aliases=["Kinkou"])
ent("shadow-order", "The Order of Shadow", "organization", "A militant Ionian order that Zed founded during the Noxian invasion. It uses forbidden shadow techniques to drive out invaders.", ["wiki-invasion", "u-zed"], aliases=["Shadow Order"])
ent("sentinels-of-light", "The Sentinels of Light", "organization", "An ancient order that fights the Black Mist. Lucian and Senna rebuilt it to stop Viego, the Ruined King.", ["wiki-ruined-king", "u-senna"])
ent("mageseekers", "The Mageseekers", "organization", "The Demacian order that hunts and imprisons mages. Sylas was its most famous prisoner.", ["wiki-mage-rebellion", "u-sylas"])
ent("winters-claw", "The Winter's Claw", "faction", "A fierce Freljordian tribe led by Sejuani that raids its neighbors to survive.", ["u-sejuani", "wiki-invasion"])
ent("avarosan", "The Avarosans", "faction", "The most populous Freljordian horde, led by Ashe. She renamed the Ebrataal tribe after her mother's old tribe.", ["u-ashe", "wiki-invasion"])
ent("frostguard", "The Frostguard", "faction", "A Freljordian order that Lissandra secretly controls from the Frostguard Citadel. It hides the truth about the Watchers.", ["u-lissandra", "wiki-three-sisters"])
ent("solari", "The Solari", "organization", "A sun-worshipping order of Mount Targon. Leona is its holy warrior.", ["u-leona", "wiki-recent"])

# --- artifacts ---
ent("world-runes", "World Runes", "artifact", "Fragments of the raw magic that shaped the world. Their misuse caused the Rune Wars, and Ryze now hunts them to keep them safe.", ["wiki-formation", "wiki-rune-wars", "u-ryze"])
ent("sun-disc", "The Sun Disc", "artifact", "The great solar structure at the heart of Shurima's capital that enabled the Ascension ritual. It sank under the sands when Azir died and rose again when he was reborn.", ["wiki-golden-age", "wiki-fall-shurima", "wiki-sun-disc"])
ent("true-ice", "True Ice", "artifact", "Ice that never melts, used by the Iceborn. Lissandra used it to entomb the Watchers, and Ashe carries a bow made of it.", ["wiki-three-sisters", "u-ashe"])
ent("petricite", "Petricite", "artifact", "A stone that nullifies magic. It sheltered the refugees who founded Demacia, and the Demacians used it to build Galio.", ["wiki-rune-wars", "wiki-resurgence"])
ent("waters-of-life", "Waters of Life", "artifact", "Blessed waters on the Blessed Isles that could heal any ailment. Viego's attempt to use them to revive Isolde caused the Ruination.", ["wiki-ruination", "wiki-westward"])
ent("hextech", "Hextech", "artifact", "Technology that harnesses magic through crystals. Jayce and Viktor first made it work in Piltover.", ["u-jayce", "wiki-arcane-s1"])
ent("shimmer", "Shimmer", "artifact", "A purple chemical made by Singed that gives great strength at a terrible cost.", ["u-singed", "wiki-arcane-s1"])
ent("rhaast", "Rhaast", "artifact", "A Darkin who was sealed in a scythe. Kayn took up the weapon and now fights its corruption.", ["u-kayn", "wiki-recent"], aliases=["the Darkin Scythe"])

# --- canon characters ---
def champ(slug, name, summary, extra=None, aliases=None, ent_slug=None):
    s = ["u-" + slug] + (extra or [])
    ent(ent_slug or slug, name, "character", summary, s, aliases=aliases)

champ("aatrox", "Aatrox", "A Darkin who once defended Shurima against the Void. Mortal sorcery sealed him in his sword, and he was the first of the Darkin to break free.", ["wiki-darkin-war"], ["the Darkin Blade"])
champ("ahri", "Ahri", "A fox-like vastaya from Ionia who can charm her prey and take their essence. She travels the world to learn about her lost ancestors.", ["wiki-ruined-king"], ["the Nine-Tailed Fox"])
champ("akali", "Akali", "An Ionian assassin who left the Kinkou Order and her title of Fist of Shadow to fight for her homeland alone.", ["wiki-recent"], ["the Rogue Assassin"])
champ("akshan", "Akshan", "A charismatic Shuriman Sentinel who can bring a victim back to life by killing their murderer. He joined the fight against Viego.", ["wiki-ruined-king"])
champ("ambessa", "Ambessa Medarda", "A ruthless Noxian general and the matriarch of the Medarda family. She is Mel's mother.", [], ["the Matriarch of War"])
champ("anivia", "Anivia", "A Freljordian demi-god in the form of an ice phoenix who is reborn again and again to protect the north.", ["wiki-formation"], ["the Cryophoenix"])
champ("annie", "Annie", "A child mage with great fire magic, raised in the mountains north of Noxus. Her bear Tibbers became a fiery protector when her powers woke.", ["wiki-recent"], ["the Dark Child"])
champ("ashe", "Ashe", "The Iceborn warmother of the Avarosans, who wields a bow of True Ice. Her people believe she is Avarosa reborn.", ["wiki-invasion"], ["the Frost Archer"])
champ("aurelionsol", "Aurelion Sol", "A celestial dragon who forged stars. The Aspects of Targon tricked him into servitude so that his power could make Shurima's god-warriors.", ["wiki-creation", "wiki-westward"], ["the Star Forger"], ent_slug="aurelion-sol")
champ("azir", "Azir", "The last emperor of ancient Shurima. Xerath murdered him during his Ascension, but millennia later he was reborn as an Ascended and raised his city from the sands.", ["wiki-fall-shurima", "wiki-sun-disc"], ["Emperor of the Sands"])
champ("bard", "Bard", "A celestial wanderer who keeps the balance between creation and the void beyond it. He is drawn to artifacts of great magic.", ["wiki-creation", "wiki-invasion"], ["the Wandering Caretaker"])
champ("belveth", "Bel'Veth", "A Void empress made from a devoured city. She plans to remake reality and to overthrow the Watchers that made her.", ["wiki-recent"], ["Empress of the Void"], ent_slug="bel-veth")
champ("braum", "Braum", "A kind-hearted Iceborn hero of the Freljord who carries a magic vault door as a shield.", ["wiki-ruined-king"], ["the Heart of the Freljord"])
champ("caitlyn", "Caitlyn", "Caitlyn Kiramman, Piltover's best peacekeeper and sharpshooter. She often works with Vi.", [], ["the Sheriff of Piltover"])
champ("cassiopeia", "Cassiopeia", "The youngest daughter of the noble Du Couteau family of Noxus. A tomb guardian's venom turned her into a serpent-like predator.", ["wiki-sun-disc"], ["the Serpent's Embrace"])
champ("darius", "Darius", "A Noxian warrior from Basilich who rose to become the Hand of Noxus. He is Draven's brother.", ["wiki-invasion"], ["the Hand of Noxus"])
champ("diana", "Diana", "A Lunari warrior who became the host of the moon's Aspect. She opposes the Solari of Mount Targon.", [], ["Scorn of the Moon"])
champ("draven", "Draven", "A showy Noxian executioner and Darius's brother. He helped Swain take power.", ["wiki-invasion"], ["the Glorious Executioner"])
champ("ekko", "Ekko", "A young genius from Zaun who uses his Z-Drive to rewind time.", [], ["the Boy Who Shattered Time"])
champ("evelynn", "Evelynn", "A demon that feeds on pain. She took form from the suffering of the Rune Wars and lures victims with a human disguise.", ["wiki-rune-wars"], ["Agony's Embrace"])
champ("ezreal", "Ezreal", "A daring Piltovan explorer who raids ancient tombs and relies on his natural magic gift.", ["wiki-recent"], ["the Prodigal Explorer"])
champ("galio", "Galio", "A petricite colossus built to guard Demacia against mages. Strong magic wakes him from his stone sleep.", ["wiki-resurgence", "wiki-mage-rebellion"], ["the Colossus"])
champ("gangplank", "Gangplank", "The fallen pirate king of Bilgewater, who wants to take his city back at any cost.", ["wiki-ruined-king"], ["the Saltwater Scourge"])
champ("garen", "Garen", "A noble Demacian soldier of the Crownguard family who leads the Dauntless Vanguard. Lux is his sister.", ["wiki-mage-rebellion"], ["the Might of Demacia"])
champ("graves", "Graves", "Malcolm Graves, a mercenary and thief who carries the shotgun Destiny. He works with his old partner Twisted Fate.", ["wiki-recent"], ["the Outlaw"])
champ("gwen", "Gwen", "A doll brought to life by magic, who fights with the Hallowed Mist and her sewing tools.", ["wiki-ruined-king"], ["the Hallowed Seamstress"])
champ("hecarim", "Hecarim", "The Camavoran knight-commander who betrayed Kalista. The Ruination fused him with his horse into a spectral rider.", ["wiki-ruination"], ["the Shadow of War"])
champ("heimerdinger", "Heimerdinger", "Professor Cecil B. Heimerdinger, a yordle inventor and the longest-serving member of the Council of Piltover.", ["wiki-recent"], ["the Revered Inventor"])
champ("illaoi", "Illaoi", "The Truth Bearer of Nagakabouros, a priestess of the Buhru faith in Bilgewater.", ["wiki-ruined-king"], ["the Kraken Priestess"])
champ("irelia", "Irelia", "A young dancer from Navori who turned her art into war and led the Ionian resistance against Noxus.", ["wiki-invasion"], ["the Blade Dancer"])
champ("janna", "Janna", "An ancient wind spirit who protects the poor of Zaun. Sailors first prayed to her in Oshra Va'Zaun.", ["wiki-westward", "wiki-resurgence"])
champ("jarvaniv", "Jarvan IV", "The crown prince of Demacia. After his father's murder he vowed to hunt down the rebel mages.", ["wiki-mage-rebellion"], ["the Exemplar of Demacia"], ent_slug="jarvan-iv")
champ("jax", "Jax", "The last of the Kohari, the guards of Icathia. He has wandered for millennia since the Void destroyed his home.", ["wiki-void-war"], ["Grandmaster at Arms"])
champ("jayce", "Jayce", "Jayce Talis, a Piltovan inventor who made the first hextech breakthroughs with his friend Viktor.", [], ["the Defender of Tomorrow"])
champ("jhin", "Jhin", "An Ionian serial killer who treats murder as art. A secret faction in Ionia's government freed him to use as its assassin.", ["wiki-recent"], ["the Virtuoso", "Khada Jhin"])
champ("jinx", "Jinx", "An impulsive criminal from Zaun who spreads chaos through Piltover with homemade weapons.", [], ["the Loose Cannon"])
champ("kaisa", "Kai'Sa", "The daughter of Kassadin, swallowed by the Void as a child. She survived by bonding with a living Void carapace.", ["wiki-recent"], ["Daughter of the Void"], ent_slug="kaisa")
champ("kalista", "Kalista", "A Camavoran general who served King Viego and was betrayed. Now she is a specter of vengeance who hunts traitors.", ["wiki-ruination"], ["the Spear of Vengeance"])
champ("kassadin", "Kassadin", "A Shuriman guide whose village the Void consumed. He hunts the Void and its prophet Malzahar.", ["wiki-recent"], ["the Void Walker"])
champ("katarina", "Katarina", "A Noxian assassin and the eldest daughter of General Du Couteau.", ["wiki-mage-rebellion"], ["the Sinister Blade"])
champ("kayle", "Kayle", "The daughter of a Targonian Aspect, born during the Rune Wars. She and her twin Morgana protected Demacia until she left the mortal world.", ["wiki-rune-wars", "wiki-resurgence"], ["the Righteous"])
champ("kayn", "Kayn", "Shieda Kayn, a shadow assassin of the Order of Shadow who wields the Darkin scythe Rhaast.", ["wiki-recent"], ["the Shadow Reaper"])
champ("leblanc", "LeBlanc", "The mysterious matron of the Black Rose, who has manipulated Noxus since its earliest days.", ["wiki-iron-revenant"], ["the Deceiver"])
champ("leona", "Leona", "A Solari warrior who carries the Aspect of the Sun.", [], ["the Radiant Dawn"])
champ("lissandra", "Lissandra", "One of the three Iceborn sisters. She made the pact with the Watchers and still rules the Frostguard in secret.", ["wiki-founding-freljord", "wiki-three-sisters"], ["the Ice Witch"])
champ("lucian", "Lucian", "A Sentinel of Light who hunts wraiths with twin relic pistols. He fought to free his wife Senna from Thresh.", ["wiki-ruined-king"], ["the Purifier"])
champ("lux", "Lux", "Luxanna Crownguard, a Demacian noble who can bend light and had to hide her magic.", ["wiki-mage-rebellion"], ["the Lady of Luminosity"])
champ("malphite", "Malphite", "A being of living stone, born from the last shard of the Ixtali Monolith that fought the Void.", ["wiki-void-war"], ["Shard of the Monolith"])
champ("malzahar", "Malzahar", "A Shuriman seer who believes the Void will save Runeterra.", ["wiki-recent"], ["the Prophet of the Void"])
champ("mel", "Mel Medarda", "The heir of the Noxian Medarda family and a skilled politician. She found she had magic after meeting the Black Rose.", [], ["the Soul's Reflection"])
champ("missfortune", "Miss Fortune", "Sarah Fortune, a Bilgewater captain who avenged her family by blowing up Gangplank's ship.", ["wiki-recent", "wiki-ruined-king"], ["the Bounty Hunter", "Sarah Fortune"], ent_slug="miss-fortune")
champ("mordekaiser", "Mordekaiser", "The warlord Sahn-Uzal, reborn as an iron revenant who built an empire in eastern Valoran.", ["wiki-iron-revenant"], ["the Iron Revenant", "Sahn-Uzal"])
champ("morgana", "Morgana", "Kayle's twin sister, who bound her wings to embrace her human side. She protects the persecuted in Demacia.", ["wiki-resurgence"], ["the Fallen"])
champ("nasus", "Nasus", "A jackal-headed Ascended scholar of Shurima, and Renekton's older brother. He went into exile after Azir's failed Ascension.", ["wiki-fall-shurima"], ["the Curator of the Sands"])
champ("olaf", "Olaf", "A Freljordian berserker who wants to die in glorious battle.", ["wiki-ruined-king"], ["the Berserker"])
champ("ornn", "Ornn", "The Freljordian demi-god of the forge, who works under the volcano Hearth-Home. In myth he is known as Ramhaurg.", ["wiki-formation", "wiki-founding-freljord"], ["the Fire Below the Mountain", "Ramhaurg"])
champ("pantheon", "Pantheon", "Atreus, once the host of the Aspect of War. He survived when the Aspect died and now opposes the divine.", ["wiki-recent"], ["the Unbreakable Spear", "Atreus"])
champ("poppy", "Poppy", "A yordle who carries Orlon's hammer and searches for the Hero of Demacia.", ["wiki-resurgence"], ["Keeper of the Hammer"])
champ("pyke", "Pyke", "A Bilgewater harpooner who came back from the deep to hunt those who exploit others.", ["wiki-ruined-king"], ["the Bloodharbor Ripper"])
champ("qiyana", "Qiyana", "An Ixtali noble with great elemental magic who wants the high seat of the Yun Tal.", ["wiki-recent"], ["Empress of the Elements"])
champ("rakan", "Rakan", "A charming vastayan battle-dancer and Xayah's partner.", [], ["the Charmer"])
champ("rell", "Rell", "A girl the Black Rose turned into a weapon. She escaped and now wants to bring down Noxus.", ["wiki-recent"], ["the Iron Maiden"])
champ("renekton", "Renekton", "An Ascended warrior of Shurima, locked in a tomb with Xerath for millennia. He now hunts his brother Nasus.", ["wiki-fall-shurima", "wiki-sun-disc"], ["the Butcher of the Sands"])
champ("riven", "Riven", "A former Noxian soldier who left the empire after the chemical attack in Navori. She now seeks redemption.", ["wiki-invasion"], ["the Exile"])
champ("ryze", "Ryze", "An ancient archmage, once Tyrus's apprentice, who hunts the World Runes to keep them from misuse.", ["wiki-ruination", "wiki-rune-wars"], ["the Rune Mage"])
champ("sejuani", "Sejuani", "The warmother of the Winter's Claw and Ashe's former battlesister.", ["wiki-invasion"], ["the Winter's Wrath"])
champ("senna", "Senna", "A Sentinel of Light who was cursed by the Black Mist. Thresh trapped her soul, and she came back as a wraith with a relic cannon.", ["wiki-ruined-king"], ["the Redeemer"])
champ("seraphine", "Seraphine", "A singer born in Piltover to Zaunite parents. She can hear the souls of others and performs for both cities.", [], ["the Starry-Eyed Songstress"])
champ("shen", "Shen", "The leader of the Kinkou Order, the Eye of Twilight.", ["wiki-recent"], ["the Eye of Twilight"])
champ("shyvana", "Shyvana", "A half-dragon warrior who saved Prince Jarvan IV and now serves in his royal guard.", ["wiki-mage-rebellion"], ["the Half-Dragon"])
champ("singed", "Singed", "A brilliant but amoral alchemist from Zaun, the maker of shimmer and the chemical weapons used in Ionia.", ["wiki-invasion"], ["the Mad Chemist"])
champ("sion", "Sion", "A Noxian warlord who strangled the Demacian king Jarvan I and was later raised from the dead.", ["wiki-first-war"], ["the Undead Juggernaut"])
champ("sivir", "Sivir", "A Shuriman mercenary captain and the last of Azir's bloodline. Her blood restored Azir.", ["wiki-sun-disc", "wiki-darkin-war"], ["the Battle Mistress"])
champ("skarner", "Skarner", "An ancient brackern who helped found Ixtal and its ruling Yun Tal, and who guards its borders.", ["wiki-westward", "wiki-rune-wars"], ["the Primordial Sovereign"])
champ("swain", "Swain", "Jericho Swain, the Grand General of Noxus. He seized power in a coup in 989 AN.", ["wiki-invasion"], ["the Noxian Grand General", "Jericho Swain"])
champ("sylas", "Sylas", "A mage from Dregbourne who escaped Mageseeker prison with Lux's power and leads a mage rebellion in Demacia.", ["wiki-mage-rebellion"], ["the Unshackled"])
champ("syndra", "Syndra", "A very powerful Ionian mage. She was freed from her prison at Fae'lor in 996 AN.", ["wiki-recent"], ["the Dark Sovereign"])
champ("taliyah", "Taliyah", "A young Shuriman stoneweaver who trained with Yasuo and went home to protect her tribe.", ["wiki-sun-disc"], ["the Stoneweaver"])
champ("thresh", "Thresh", "Erlok Grael, once a warden of Helia, now a cruel specter who collects souls in his lantern.", ["wiki-ruination", "wiki-ruined-king"], ["the Chain Warden", "Erlok Grael"])
champ("twistedfate", "Twisted Fate", "A cardsharp and swindler who works with his old partner Graves.", ["wiki-recent"], ["the Card Master"], ent_slug="twisted-fate")
champ("varus", "Varus", "One of the Darkin, the last to be sealed at the end of the Great Darkin War. He escaped in the bodies of two Ionian hunters.", ["wiki-darkin-war"], ["the Arrow of Retribution"])
champ("vayne", "Vayne", "Shauna Vayne, a Demacian monster hunter who seeks the demon that killed her family.", ["wiki-recent", "wiki-ruined-king"], ["the Night Hunter"])
champ("veigar", "Veigar", "A yordle sorcerer whose curiosity turned dark during his long imprisonment in the Immortal Bastion.", ["wiki-iron-revenant"], ["the Tiny Master of Evil"])
champ("velkoz", "Vel'Koz", "A cold, curious Voidborn, made as one of the first Void prototypes during the War of the Three Sisters.", ["wiki-three-sisters"], ["the Eye of the Void"], ent_slug="vel-koz")
champ("vi", "Vi", "A brawler from Zaun with hextech gauntlets. She now works with the Piltover enforcers.", [], ["the Piltover Enforcer"])
champ("viego", "Viego", "The king of Camavor whose attempt to revive his queen caused the Ruination. He returned as the Ruined King.", ["wiki-ruination", "wiki-ruined-king"], ["the Ruined King"])
champ("viktor", "Viktor", "A Zaunite inventor and Jayce's former partner. He gave up his humanity for his Glorious Evolution.", [], ["Herald of the Arcane", "the Machine Herald"])
champ("vladimir", "Vladimir", "A blood mage who learned hemomancy from a Darkin. He has shaped Noxus since its earliest days.", ["wiki-darkin-war", "wiki-iron-revenant"], ["the Crimson Reaper"])
champ("volibear", "Volibear", "The Freljordian demi-god of storms, known in myth as Valhir. He hates civilization.", ["wiki-founding-freljord"], ["the Relentless Storm", "Valhir"])
champ("warwick", "Warwick", "A monster of Zaun, made by cruel experiments and fused with machines that pump rage into his veins.", [], ["the Uncaged Wrath of Zaun"])
champ("xayah", "Xayah", "A vastayan rebel who fights with feather blades beside her partner and lover Rakan.", [], ["the Rebel"])
champ("xerath", "Xerath", "A former slave who became an Ascended Magus by betraying Azir. He was sealed under the sands for millennia.", ["wiki-fall-shurima"], ["the Magus Ascendant"])
champ("xinzhao", "Xin Zhao", "A former Noxian pit fighter who swore loyalty to Demacia's royal family.", ["wiki-invasion", "wiki-mage-rebellion"], ["the Seneschal of Demacia"], ent_slug="xin-zhao")
champ("yasuo", "Yasuo", "An Ionian swordsman who was falsely accused of murdering his master and forced to kill his brother.", ["wiki-invasion"], ["the Unforgiven"])
champ("yone", "Yone", "Yasuo's half-brother, killed by him and then forced to wear a demon's mask in the spirit realm.", ["wiki-ruined-king"], ["the Unforgotten"])
champ("yorick", "Yorick", "The last monk of a forgotten order on the Shadow Isles who can speak with the dead.", ["wiki-ruination", "wiki-ruined-king"], ["Shepherd of Souls"])
champ("zed", "Zed", "The ruthless founder of the Order of Shadow, who uses forbidden shadow magic.", ["wiki-invasion", "wiki-recent"], ["the Master of Shadows"])
champ("zeri", "Zeri", "A spirited young woman from Zaun who uses electric magic.", ["wiki-recent"], ["the Spark of Zaun"])
champ("zilean", "Zilean", "An Icathian council member and time mage who pulled his tower and his people out of time when the Void came.", ["wiki-golden-age", "wiki-void-war"], ["the Chronokeeper"])
champ("zoe", "Zoe", "The playful Aspect of Twilight and a cosmic messenger of Targon.", ["wiki-darkin-war", "wiki-recent"], ["the Aspect of Twilight"])
champ("lulu", "Lulu", "A yordle mage who makes dreamlike illusions and travels with her fairy Pix.", ["wiki-recent"], ["the Fae Sorceress"])

# canon non-champion characters
ent("isolde", "Isolde", "character", "A seamstress who married King Viego. She was poisoned by an assassin's blade, and her return as a wraith in the Well of Ages set off the Ruination.", ["wiki-ruination"])
ent("tyrus", "Tyrus", "character", "A Seeker Adept of Helia and Ryze's master. He survived the Ruination but later tried to use World Runes, and Ryze killed him.", ["wiki-ruination", "wiki-rune-wars"])
ent("avarosa", "Avarosa", "character", "One of the three Iceborn sisters who united the Freljord. Lissandra sacrificed her and her armies to entomb the Watchers.", ["wiki-founding-freljord", "wiki-three-sisters"])
ent("serylda", "Serylda", "character", "The third Iceborn sister, who died with Avarosa at the Howling Abyss.", ["wiki-founding-freljord", "wiki-three-sisters"])
ent("nagakabouros", "Nagakabouros", "character", "The spirit god of the ocean and of motion, worshipped by the Buhru. Illaoi serves it.", ["wiki-formation", "wiki-westward", "u-illaoi"], aliases=["the Mother Serpent", "the Great Kraken"])
ent("kusho", "Master Kusho", "character", "A Kinkou master who trained Zed and Shen. He faked his death, secretly freed Jhin, and was killed by Zed.", ["wiki-recent", "wiki-invasion"])
ent("boram-darkwill", "Boram Darkwill", "character", "The Grand General of Noxus who ordered the invasion of Ionia. Swain deposed and killed him in 989 AN.", ["wiki-invasion"])
ent("jarvan-i", "Jarvan I", "character", "A Demacian king whom Sion killed with his bare hands at Hvardis.", ["wiki-first-war"])
ent("jarvan-iii", "Jarvan III", "character", "The king of Demacia and Jarvan IV's father. He was assassinated in 996 AN during the mage revolt.", ["wiki-mage-rebellion", "wiki-invasion"])

# ======================= AU ENTITIES =======================
# K/DA
ent("kda", "K/DA", "organization", "A virtual K-pop girl group made of Ahri, Akali, Evelynn and Kai'Sa. Riot Games unveiled it at the 2018 World Championship.", ["wp-kda", "wiki-kda"], timeline="kda")
ent("kda-ahri", "K/DA Ahri", "character", "The leader and founder of K/DA and one of its main vocalists. Her solo song on ALL OUT is 'I'll Show You'.", ["wp-kda", "wiki-kda"], timeline="kda", variant_of="ahri")
ent("kda-akali", "K/DA Akali", "character", "The group's main rapper, with the solo track 'The Baddest'. She later started a side project to recruit new talent.", ["wp-kda", "wiki-kda"], timeline="kda", variant_of="akali")
ent("kda-evelynn", "K/DA Evelynn", "character", "A main vocalist known for her diva attitude. She clashed with earlier groups and wrote alone before she rejoined Ahri to form K/DA. Her solo song is 'Villain'.", ["wp-kda"], timeline="kda", variant_of="evelynn")
ent("kda-kaisa", "K/DA Kai'Sa", "character", "The group's main dancer, a quiet loner who speaks through movement. Her solo song is 'Drum Go Dum'. In this setting Kassadin is only her dad.", ["wp-kda", "wiki-kda"], timeline="kda", variant_of="kaisa")
ent("kda-seraphine", "K/DA Seraphine", "character", "A Chinese-American indie singer in Los Angeles whose posts caught K/DA's attention. She is a guest artist on 'More', not a permanent member.", ["wp-kda", "wp-more", "wiki-kda"], timeline="kda", variant_of="seraphine")
# Star Guardian
ent("star-guardians", "The Star Guardians", "organization", "Young warriors chosen by the First Star to protect the light of the stars. Their power burns bright but often ends in tragedy.", ["wiki-star-guardian"], timeline="star-guardian")
ent("sg-lux", "Star Guardian Lux", "character", "A Valoran City High student who leads the first Star Guardian team of the series, with Janna as mentor.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="lux")
ent("sg-janna", "Star Guardian Janna", "character", "A veteran guardian from an older team who mentors Lux's squad.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="janna")
ent("sg-jinx", "Star Guardian Jinx", "character", "A member of Lux's team in Season 1.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="jinx")
ent("sg-ahri", "Star Guardian Ahri", "character", "A veteran leader who rebuilt her team after her first squad was destroyed, and returned to Valoran City in Season 2.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="ahri")
ent("sg-miss-fortune", "Star Guardian Miss Fortune", "character", "Ahri's long-time teammate on both her original and later teams.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="miss-fortune")
ent("sg-zoe", "Star Guardian Zoe", "character", "An ancient guardian whom grief over losing a teammate corrupted into the Twilight Star, the main threat of Season 3.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="zoe", aliases=["the Twilight Star"])
ent("sg-xayah", "Star Guardian Xayah", "character", "A member of Ahri's original team who fell, came back in Season 3, and was redeemed. She leads her own team in Season 4.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="xayah")
ent("sg-rakan", "Star Guardian Rakan", "character", "A member of Ahri's original team who fell with Xayah and was later redeemed and healed.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="rakan")
ent("sg-kaisa", "Star Guardian Kai'Sa", "character", "Co-leader, with Akali, of the new team that defends a Valoran City scarred by Zoe's invasion in Season 4.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="kaisa")
ent("sg-akali", "Star Guardian Akali", "character", "Co-leader of Kai'Sa's team in Season 4.", ["wiki-star-guardian"], timeline="star-guardian", variant_of="akali")
# Arcane
ent("firelights", "The Firelights", "organization", "A Zaunite rebel group led by Ekko in Arcane.", ["wp-arcane", "wiki-arcane-s1"], timeline="arcane")
ent("arcane-vi", "Vi (Arcane)", "character", "A Zaunite orphan raised by Vander and Powder's older sister. After years in Stillwater she fights beside Caitlyn and becomes her love interest.", ["wp-arcane", "wiki-arcane-s1"], timeline="arcane", variant_of="vi", aliases=["Violet"])
ent("arcane-jinx", "Jinx (Arcane)", "character", "Powder, Vi's younger sister. Silco raised her after her bomb killed Mylo and Claggor, and she became Jinx.", ["wp-arcane", "wiki-arcane-s1"], timeline="arcane", variant_of="jinx", aliases=["Powder"])
ent("arcane-caitlyn", "Caitlyn (Arcane)", "character", "Caitlyn Kiramman, a Piltover enforcer and Jayce's former lab assistant. She leads a strike team after her mother dies.", ["wp-arcane", "arcwiki-s2e1"], timeline="arcane", variant_of="caitlyn")
ent("arcane-jayce", "Jayce (Arcane)", "character", "Jayce Talis, the inventor of hextech who becomes a Piltover councilor.", ["wp-arcane", "wiki-arcane-s1"], timeline="arcane", variant_of="jayce")
ent("arcane-viktor", "Viktor (Arcane)", "character", "A sick Zaunite scientist and Jayce's partner. Hextech and the hexcore transform him into the Herald of a Glorious Evolution.", ["wp-arcane", "arcwiki-s2e8"], timeline="arcane", variant_of="viktor")
ent("arcane-silco", "Silco", "character", "A Zaunite crime lord, leader of the Chem-Barons, and Jinx's adoptive father. He was once Vander's brother-in-arms.", ["wp-arcane", "wiki-arcane-s1"], timeline="arcane")
ent("arcane-vander", "Vander (Arcane)", "character", "A former rebel who runs The Last Drop and adopts Vi and Powder. Singed later turns him into the beast Warwick.", ["wp-arcane", "arcwiki-s2e6"], timeline="arcane", variant_of="warwick", aliases=["Warwick"])
ent("arcane-ekko", "Ekko (Arcane)", "character", "Vi and Powder's childhood friend, who grows up to lead the Firelights.", ["wp-arcane", "wiki-arcane-s1"], timeline="arcane", variant_of="ekko")
ent("arcane-heimerdinger", "Heimerdinger (Arcane)", "character", "A founder of Piltover and head of its council who mentors Jayce, Viktor and later Ekko.", ["wp-arcane", "wiki-arcane-s1"], timeline="arcane", variant_of="heimerdinger")
ent("arcane-mel", "Mel (Arcane)", "character", "Mel Medarda, a Piltover councilor and Ambessa's exiled heir. She backs Jayce's work and begins a romance with him.", ["wp-arcane", "wiki-arcane-s1"], timeline="arcane", variant_of="mel")
ent("arcane-ambessa", "Ambessa (Arcane)", "character", "Mel's mother, a Noxian general who wants hextech weapons to fight the Black Rose.", ["wp-arcane", "arcwiki-s2e3"], timeline="arcane", variant_of="ambessa")
ent("arcane-singed", "Singed (Arcane)", "character", "Dr. Corin Reveck, the chemist behind shimmer. He works for Silco and then Ambessa and wants to cure death to save his daughter.", ["wp-arcane", "arcwiki-s2e8"], timeline="arcane", variant_of="singed")
ent("arcane-sevika", "Sevika", "character", "Silco's right-hand enforcer. She joins the reformed Piltover council after the war.", ["wp-arcane", "arcwiki-s2e9"], timeline="arcane")
ent("arcane-leblanc", "LeBlanc (Arcane)", "character", "The Illusionary Sorceress of the Black Rose, who entangles Mel and fights Ambessa.", ["wp-arcane", "arcwiki-s2e9"], timeline="arcane", variant_of="leblanc", aliases=["the Illusionary Sorceress"])

# ======================= EVENTS =======================
events = []
def ev(slug, timeline, title, summary, date_label, sort_key, era, importance, parts, sources_):
    events.append({"slug": slug, "timeline": timeline, "title": title, "summary": summary, "date_label": date_label,
                   "sort_key": sort_key, "era": era, "importance": importance,
                   "participants": [{"entity": e, "role": r} for e, r in parts], "sources": sources_})

R = "runeterra"
ERA_PRIM = "Primordial Age"
ERA_ANC = "Ancient Age"
ERA_SHU = "Shuriman Empire"
ERA_DAR = "Darkin Age"
ERA_RUN = "Ruination and Rune Wars"
ERA_RES = "Resurgence of Civilizations"
ERA_WAR = "Demacian-Noxian Wars"
ERA_REC = "Recent History"

ev("creation-of-the-universe", R, "Creation of the Universe", "Reality burst into the emptiness of the Void, and with it came the first Celestials such as Aurelion Sol and Bard. The expansion woke the Watchers, who resent the existence of everything.", "∞ BN", -100000, ERA_PRIM, 5, [("aurelion-sol", "creator"), ("bard", "witness"), ("watchers", "antagonist"), ("void", "origin")], ["wiki-creation"])
ev("forging-of-runeterra", R, "Forging of Runeterra", "Unknown beings used the World Runes to shape Runeterra, which formed a physical realm and a spirit realm. Spirit gods, demons and the first yordles appeared, followed later by mortal races.", "∞ BN – c. 9000 BN", -50000, ERA_PRIM, 5, [("runeterra", "subject"), ("world-runes", "instrument"), ("nagakabouros", "witness"), ("bandle-city", "founded")], ["wiki-creation", "wiki-formation"])
ev("titan-war", R, "Titan War", "Mortals of Ionia fought sky-giants who came from above. Enlightened mortals took spirit power into themselves and became the Vastayashai'rei, the ancestors of the vastaya, and they won the war.", "c. 9000 BN", -9000, ERA_ANC, 3, [("ionia", "location")], ["wiki-titan-war"])
ev("lissandra-pact-with-watchers", R, "Lissandra's Pact with the Watchers", "Blinded by the demi-god Valhir, Lissandra reached the Watchers through dreamwalking. She traded near-immortality and rule of the Freljord for preparing the world for the Void, and the Three Sisters then fought the old gods.", "c. 9000–8000 BN", -8500, ERA_ANC, 4, [("lissandra", "instigator"), ("watchers", "ally"), ("volibear", "enemy"), ("avarosa", "participant"), ("serylda", "participant")], ["wiki-founding-freljord"])
ev("war-of-the-three-sisters", R, "War of the Three Sisters", "Avarosa and Serylda marched on Lissandra's citadel to resist serving the Watchers, just as the Watchers began to emerge. Lissandra sacrificed her sisters and their armies to entomb the Watchers in True Ice under the Howling Abyss.", "8000 BN", -8000, ERA_ANC, 5, [("lissandra", "instigator"), ("avarosa", "victim"), ("serylda", "victim"), ("watchers", "imprisoned"), ("true-ice", "instrument"), ("vel-koz", "created")], ["wiki-three-sisters", "u-region-freljord"])
ev("westward-migration", R, "Westward Migration", "Settlers from a lost eastern continent crossed to Shurima and Valoran over a thousand years. They founded the Buhru of the Serpent Isles, Helia on the Blessed Isles, Ixtal, the first Shuriman capital, the Targonian theocracy, Oshra Va'Zaun and Icathia.", "6000–5000 BN", -6000, ERA_ANC, 4, [("shurima", "founded"), ("ixtal", "founded"), ("helia", "founded"), ("icathia", "founded"), ("mount-targon", "settled"), ("zaun", "founded"), ("skarner", "founder")], ["wiki-westward", "u-region-ixtal"])
ev("first-ascended", R, "Rise of the God-Warriors", "Guided by the Aspects of Targon, Shurimans used a Sun Disc to create the first Ascended. These god-warriors were worshipped as living gods and built an empire that lasted for millennia.", "c. 5000 BN", -5000, ERA_SHU, 5, [("ascended", "created"), ("sun-disc", "instrument"), ("shurima", "location"), ("aurelion-sol", "power source")], ["wiki-golden-age", "u-aurelionsol"])
ev("conquest-of-icathia", R, "Shurima Conquers Icathia", "The Shuriman Ascended subjugated the mage kingdom of Icathia and killed its mage king Axamuk. Shurima then banned the worship of any deity except the Ascended.", "3400 BN", -3400, ERA_SHU, 3, [("shurima", "aggressor"), ("icathia", "victim"), ("ascended", "aggressor")], ["wiki-golden-age"])
ev("void-war", R, "Icathian Rebellion and the Void War", "Icathia rebelled against Shurima and tried to weaponize the Void, but tore open a huge rift that destroyed its own capital. Ascended and Voidborn fought a long war, and Zilean pulled his tower full of refugees out of time.", "c. 2500 BN", -2500, ERA_SHU, 5, [("icathia", "instigator"), ("void", "unleashed"), ("ascended", "defender"), ("jax", "combatant"), ("zilean", "witness"), ("aatrox", "combatant")], ["wiki-void-war", "u-region-void", "u-jax"])
ev("fall-of-the-monolith", R, "Fall of the Monolith", "The Ixtali god-warrior Ne'Zuk built the Monolith, a floating fortress, to fight the Void in Icathia. It crashed into the rift, and its last surviving shard later became Malphite.", "c. 2500–2000 BN", -2400, ERA_SHU, 3, [("ixtal", "combatant"), ("malphite", "origin"), ("void", "enemy")], ["wiki-void-war", "u-malphite"])
ev("fall-of-shurima", R, "Fall of Shurima", "Xerath disrupted Azir's Ascension ritual, killed the emperor and ascended in his place. The magical fallout destroyed the capital and buried it and the Sun Disc under the sands. Xerath and Renekton were sealed in the Tomb of the Emperors, and Nasus went into exile.", "2000 BN", -2000, ERA_SHU, 5, [("xerath", "instigator"), ("azir", "victim"), ("renekton", "imprisoned"), ("nasus", "witness"), ("sun-disc", "lost"), ("shurima", "location")], ["wiki-fall-shurima", "u-azir"])
ev("rise-of-the-darkin", R, "Rise of the Darkin", "With no emperor and no Void to fight, many surviving Ascended became tyrants who enslaved mortals. People called them the Darkin, and they began to war with each other.", "2000–550 BN", -1500, ERA_DAR, 4, [("darkin", "instigator"), ("aatrox", "instigator"), ("ascended", "transformed")], ["wiki-darkin-war", "u-aatrox"])
ev("vladimir-learns-hemomancy", R, "Vladimir Learns Blood Magic", "Vladimir's father gave him to a Darkin to protect Camavor. The Darkin made Vladimir the first human blood mage, and Vladimir destroyed his father's kingdom on his master's orders.", "2000–550 BN", -1000, ERA_DAR, 2, [("vladimir", "protagonist"), ("darkin", "mentor"), ("camavor", "location")], ["wiki-darkin-war"])
ev("sealing-of-the-darkin", R, "End of the Great Darkin War", "Mortals given knowledge by the Aspects sealed the remaining Darkin, including Aatrox and Rhaast, inside their own weapons. Varus was the last to be sealed, in his bow, which ended the war.", "550 BN", -550, ERA_DAR, 5, [("darkin", "defeated"), ("aatrox", "sealed"), ("varus", "sealed"), ("rhaast", "sealed"), ("zoe", "ally"), ("pantheon", "ally")], ["wiki-darkin-war"])
ev("mordekaiser-reborn", R, "Mordekaiser Reborn", "Sorcerers raised the dead warlord Sahn-Uzal in a body of dark iron, hoping to use him as a weapon. He killed them, took the name Mordekaiser and began building an empire around the Immortal Bastion.", "400 BN", -400, ERA_DAR, 4, [("mordekaiser", "protagonist"), ("immortal-bastion", "built")], ["wiki-iron-revenant", "u-mordekaiser"])
ev("veigar-imprisoned", R, "Veigar Imprisoned in the Bastion", "Mordekaiser captured the curious yordle Veigar among a group of Noxii star mages. He bound Veigar to the physical plane and forced him to make dark spells for centuries.", "400–100 BN", -300, ERA_DAR, 2, [("mordekaiser", "captor"), ("veigar", "victim"), ("immortal-bastion", "location")], ["wiki-iron-revenant", "u-veigar"])
ev("founding-of-the-black-rose", R, "LeBlanc and Vladimir Found the Black Rose", "During Mordekaiser's reign, a LeBlanc visited the blood mage Vladimir on the cliffs of eastern Valoran. Their meeting and shared dark magic became the basis of the Black Rose, with LeBlanc as its matron.", "400–100 BN", -250, ERA_DAR, 3, [("leblanc", "founder"), ("vladimir", "founder"), ("black-rose", "founded")], ["wiki-iron-revenant"])
ev("fall-of-mordekaiser", R, "Fall of Mordekaiser", "An alliance of Noxii tribes, aided by a LeBlanc from his own inner circle, cut his soul from his armor and hid the empty shell. His soul went to the realm of the dead, and the Noxii inherited his empire.", "c. 100 BN", -100, ERA_DAR, 4, [("mordekaiser", "defeated"), ("leblanc", "instigator"), ("noxus", "successor")], ["wiki-iron-revenant", "u-mordekaiser"])
ev("poisoning-of-isolde", R, "Poisoning of Queen Isolde", "Plotters sent an assassin against the new king Viego. Kalista saved him, but the poisoned blade struck his queen Isolde, and Viego sent Kalista to find the Waters of Life.", "27–25 BN", -26, ERA_RUN, 3, [("viego", "target"), ("isolde", "victim"), ("kalista", "defender"), ("camavor", "location")], ["wiki-ruination"])
ev("kalista-reaches-helia", R, "Kalista Reaches the Blessed Isles", "With the help of Tyrus and his apprentice Ryze, Kalista passed the mists and pleaded with the masters of Helia, who refused her. Erlok Grael secretly offered her the Waters of Life and a waystone in exchange for influence in Camavor.", "25 BN", -25.6, ERA_RUN, 3, [("kalista", "protagonist"), ("tyrus", "ally"), ("ryze", "ally"), ("thresh", "manipulator"), ("helia", "location")], ["wiki-ruination"])
ev("the-ruination", R, "The Ruination", "Viego came to Helia with Isolde's body, and Hecarim's knights sacked the city and killed Kalista. Isolde woke as a wraith in the Well of Ages and stabbed Viego, and the unstable World Rune below released a blast that turned the Blessed Isles into the Shadow Isles under the Black Mist.", "25 BN", -25, ERA_RUN, 5, [("viego", "instigator"), ("isolde", "victim"), ("kalista", "victim"), ("hecarim", "aggressor"), ("thresh", "manipulator"), ("yorick", "witness"), ("helia", "destroyed"), ("shadow-isles", "created"), ("waters-of-life", "instrument")], ["wiki-ruination", "u-viego", "u-region-shadow-isles"])
ev("battle-of-khom", R, "Destruction of Khom", "Two Noxii nations parleyed with Tyrus at the village of Khom, and the encounter ended with two World Runes destroying the region. It was the first great attack of the Rune Wars, witnessed by Ryze.", "13 BN", -13, ERA_RUN, 5, [("tyrus", "participant"), ("ryze", "witness"), ("world-runes", "instrument")], ["wiki-rune-wars"])
ev("birth-of-kayle-and-morgana", R, "Birth of Kayle and Morgana", "Seeking divine help during the Rune Wars, the pregnant Mihira climbed Mount Targon and became the host of the Aspect of Justice. She gave birth to the twins Kayle and Morgana that year.", "13–3 BN", -10, ERA_RUN, 3, [("kayle", "born"), ("morgana", "born"), ("mount-targon", "location")], ["wiki-rune-wars", "u-kayle"])
ev("ixtal-closes-borders", R, "Ixtal Seals Its Borders", "As the Rune Wars came near, Skarner persuaded the Yun Tal to draw the wilderness around Ixaocan as a shield. Ixtal cut itself off from the rest of Runeterra.", "13–3 BN", -9, ERA_RUN, 3, [("skarner", "instigator"), ("ixtal", "subject")], ["wiki-rune-wars", "u-skarner"])
ev("ryze-slays-tyrus", R, "Ryze Kills Tyrus", "When Tyrus tried to use two World Runes for himself, his apprentice Ryze confronted and killed him. Ryze vowed never to use a World Rune and to keep them all from misuse.", "13–3 BN", -8, ERA_RUN, 4, [("ryze", "instigator"), ("tyrus", "victim"), ("world-runes", "subject")], ["wiki-rune-wars", "u-ryze"])
ev("founding-of-zeffira", R, "Refugees Found Demacia", "Refugees from the Rune Wars found shelter in forests of magic-nullifying petricite in western Valoran. There they built Zeffira, the first Demacian city.", "13–3 BN", -7, ERA_RUN, 4, [("demacia", "founded"), ("petricite", "instrument")], ["wiki-rune-wars", "u-region-demacia"])
ev("noxus-endures", R, "Noxus Endures", "The last Noxii sheltered from the magical fallout inside the Immortal Bastion. When they came out they united as one people, Noxus, and they date their calendar from this moment.", "0 AN", 0, ERA_RES, 5, [("noxus", "founded"), ("immortal-bastion", "location")], ["wiki-resurgence", "wiki-timeline", "u-region-noxus"])
ev("winged-sisters-split", R, "Kayle and Morgana Leave Demacia", "The twins defended young Demacia, but their trust broke. Their battle over the city ended when their father Kilam died, after which Kayle went to Targon and Morgana stayed in the wilds. Demacia kept their image as its crest.", "0–292 AN", 200, ERA_RES, 3, [("kayle", "combatant"), ("morgana", "combatant"), ("demacia", "location")], ["wiki-resurgence"])
ev("demacian-crown", R, "The Demacian Crown", "The nation founded by the champion Orlon crowned its first king and declared itself a sanctuary from magic forever.", "292 AN", 292, ERA_RES, 4, [("demacia", "subject"), ("poppy", "witness")], ["wiki-resurgence"])
ev("galio-built", R, "Durand Builds Galio", "Demacia asked the sculptor Durand for a moving petricite shield. He built Galio, a winged colossus that stopped an invading order of war-mages and then went still.", "292–349 AN", 320, ERA_RES, 3, [("galio", "created"), ("demacia", "creator"), ("petricite", "material")], ["wiki-resurgence", "u-galio"])
ev("noxus-becomes-empire", R, "Noxus Becomes an Imperial Power", "After forced annexations and the fall of the Drakkengate, the noble houses vowed to unite all of Runeterra under one banner. They chose a Grand General to lead their armies.", "349 AN", 349, ERA_RES, 4, [("noxus", "subject")], ["wiki-resurgence"])
ev("oshra-vazaun-disaster", R, "Tragedy on the River Pilt", "Oshra Va'Zaun used chemtech bombs to cut a sea passage through the isthmus. The blasts set off earthquakes that sank whole districts and released poison gas, and the wind spirit Janna saved many people.", "772 AN", 772, ERA_RES, 4, [("zaun", "victim"), ("janna", "savior")], ["wiki-resurgence", "u-janna"])
ev("founding-of-bilgewater", R, "Founding of Bilgewater", "Buhru missionaries let fortune seekers from Demacia, the Freljord and Ionia settle in the southern bays of the Serpent Isles. The settlement grew into Bilgewater.", "787 AN", 787, ERA_RES, 3, [("bilgewater", "founded"), ("nagakabouros", "patron")], ["wiki-resurgence", "u-region-bilgewater"])
ev("sun-gates-and-piltover", R, "Sun Gates Open; Piltover Rises", "The rebuilt city built the Sun Gates to control the new sea passage. The wealth from them created a merchant district over the Pilt River, named Piltover, and Progress Day marks the gates' opening.", "c. 790 AN", 790, ERA_RES, 4, [("piltover", "founded"), ("zaun", "parent")], ["wiki-resurgence", "u-region-piltover"])
ev("death-of-jarvan-i", R, "Sion Kills King Jarvan I", "As Demacia drove the Noxian warbands back to Hvardis, Sion threw his commander from the walls and charged. Pierced many times, he strangled King Jarvan I before he died, and Demacia retreated.", "892–895 AN", 894, ERA_WAR, 4, [("sion", "instigator"), ("jarvan-i", "victim"), ("noxus", "aggressor"), ("demacia", "defender")], ["wiki-first-war", "u-sion"])
ev("noxus-annexes-basilich", R, "Noxus Expands South", "Grand General Darkwill pushed Noxus toward the Great Barrier and annexed Basilich. Minotaurs who refused to ally, like Alistar, went to the arenas, and the orphans Darius and Draven joined the army.", "974 AN", 974, ERA_REC, 2, [("boram-darkwill", "instigator"), ("darius", "recruit"), ("draven", "recruit"), ("noxus", "aggressor")], ["wiki-invasion"])
ev("xin-zhao-joins-demacia", R, "Xin Zhao Joins Demacia", "Noxus sent conscripted pit fighters against the rebel fortress of Kalstead. Demacia beat them and spared them, and the reckoner Xin Zhao swore loyalty to King Jarvan III as his guard.", "976 AN", 976, ERA_REC, 2, [("xin-zhao", "protagonist"), ("jarvan-iii", "lord"), ("demacia", "ally")], ["wiki-invasion", "u-xinzhao"])
ev("capture-of-jhin", R, "Capture of Khada Jhin", "Master Kusho, Shen and Zed tracked the serial killer Jhin for years. They caught him at Jyom Pass and imprisoned him in Tuula.", "980 AN", 980, ERA_REC, 2, [("kusho", "hunter"), ("shen", "hunter"), ("zed", "hunter"), ("jhin", "captured")], ["wiki-recent", "u-jhin"])
ev("noxian-invasion-of-ionia", R, "Noxian Invasion of Ionia", "Grand General Boram Darkwill ordered a large-scale occupation of Ionia. Resistance grew after Admiral Duqal's forces killed Irelia's family and she found the war power of her dances.", "984 AN", 984, ERA_REC, 5, [("noxus", "aggressor"), ("ionia", "victim"), ("boram-darkwill", "instigator"), ("irelia", "resistance")], ["wiki-invasion", "u-irelia"])
ev("zed-founds-shadow-order", R, "Zed Takes the Tears of Shadow", "Banished for learning forbidden shadow techniques, Zed returned to the Kinkou temple and took the Tears of Shadow. He and Kusho staged Kusho's death, and Zed formed the Order of Shadow.", "986 AN", 986, ERA_REC, 4, [("zed", "instigator"), ("kusho", "conspirator"), ("shadow-order", "founded"), ("kinkou-order", "victim")], ["wiki-invasion", "u-zed"])
ev("kaisa-taken-by-void", R, "Kai'Sa Lost to the Void", "A Void rift opened in Kai'Sa's village and the earth swallowed it under the Sai desert. The child survived when a voidling fused to her skin, and her father Kassadin thought he had lost her.", "986 AN", 986.5, ERA_REC, 4, [("kaisa", "victim"), ("kassadin", "bereaved"), ("void", "aggressor")], ["wiki-recent", "u-kaisa"])
ev("navori-chemical-attack", R, "Chemical Attack at Navori", "Singed's chem-bombs, brought by Riven's warband, killed everyone on both sides and destroyed Master Yi's village. In the aftermath Riven caused Elder Souma's death by accident, and Yasuo was blamed for the murder.", "987 AN", 987, ERA_REC, 4, [("singed", "weapon maker"), ("riven", "survivor"), ("yasuo", "accused"), ("noxus", "aggressor"), ("ionia", "victim")], ["wiki-invasion", "u-riven", "u-yasuo"])
ev("ashe-finds-true-ice-bow", R, "Ashe Finds the True Ice Bow", "On her mother's quest for Avarosa's Throne, Ashe lost her tribe to an ambush. At the end of the maps she found a bow of True Ice and later founded a new Avarosan tribe after breaking with Sejuani.", "987 AN", 987.3, ERA_REC, 3, [("ashe", "protagonist"), ("sejuani", "rival"), ("avarosan", "founded"), ("true-ice", "artifact")], ["wiki-invasion", "u-ashe"])
ev("evelynn-kills-vaynes-parents", R, "Evelynn Kills Vayne's Parents", "The demon Evelynn murdered Shauna Vayne's parents. Vayne vowed to learn all about dark magic to take revenge.", "987 AN", 987.5, ERA_REC, 2, [("evelynn", "killer"), ("vayne", "bereaved")], ["wiki-recent", "u-vayne"])
ev("trifarian-revolution", R, "Trifarian Revolution", "The disgraced general Jericho Swain, with Draven, General Du Couteau and others, staged a coup in the capital and killed Boram Darkwill. Within a year Swain ended most of the occupation of Ionia and set up the Trifarix council.", "989 AN", 989, ERA_REC, 5, [("swain", "instigator"), ("boram-darkwill", "victim"), ("draven", "ally"), ("noxus", "location")], ["wiki-invasion", "u-swain"])
ev("battle-of-dalu-bay", R, "Battle of Dalu Bay", "Irelia's forces won a decisive victory over Admiral Duqal and ended the invasion. She then left the leadership of the resistance, and groups like the Order of Shadow fought for power.", "989 AN", 989.1, ERA_REC, 4, [("irelia", "victor"), ("ionia", "victor"), ("noxus", "defeated"), ("shadow-order", "rising faction")], ["wiki-invasion"])
ev("tomb-of-the-emperors-opened", R, "The Tomb of the Emperors Opened", "Cassiopeia betrayed Sivir and used her blade as a key to the tomb. The guardian's curse turned Cassiopeia into a serpent, and Xerath and Renekton were freed.", "989 AN", 989.2, ERA_REC, 4, [("cassiopeia", "instigator"), ("sivir", "victim"), ("xerath", "freed"), ("renekton", "freed")], ["wiki-sun-disc", "u-cassiopeia"])
ev("rebirth-of-azir", R, "Rebirth of the Sun Disc", "Sivir's blood, the last of Azir's line, restored Azir. He saved her life at the Oasis of the Dawn, became an Ascended, and raised the Sun Disc and his capital from the sands.", "989 AN", 989.3, ERA_REC, 5, [("azir", "protagonist"), ("sivir", "catalyst"), ("sun-disc", "restored"), ("shurima", "location")], ["wiki-sun-disc", "u-azir"])
ev("shyvana-saves-jarvan", R, "Shyvana Saves Jarvan IV", "Prince Jarvan IV was encircled and defeated beyond the Argent Mountains. The half-dragon Shyvana found him, carried him to safety, and killed her dragon mother Yvva to protect him.", "990 AN", 990, ERA_REC, 3, [("jarvan-iv", "rescued"), ("shyvana", "rescuer"), ("noxus", "enemy")], ["wiki-mage-rebellion", "u-shyvana"])
ev("death-of-senna", R, "Thresh Takes Senna", "While Senna and Lucian searched a vault for a cure to her curse, Thresh attacked. Senna stepped in front of her husband, and Thresh sealed her soul in his lantern.", "991 AN", 991, ERA_REC, 4, [("thresh", "killer"), ("senna", "victim"), ("lucian", "witness")], ["wiki-ruined-king", "u-senna"])
ev("fall-of-gangplank", R, "Fall of Gangplank", "Sarah Fortune took her revenge on the reaver king who had killed her parents by blowing up his flagship. Six months after his fall she removed several corrupt leaders and began to take control of Bilgewater.", "before 993 AN", 992.5, ERA_REC, 4, [("miss-fortune", "instigator"), ("gangplank", "victim"), ("bilgewater", "location")], ["wiki-ruined-king", "u-missfortune", "u-gangplank"])
ev("harrowing-of-bilgewater", R, "The Harrowing of Bilgewater", "Hecarim and Thresh led a Harrowing against Bilgewater. Illaoi called on Nagakabouros to drive it back, and Lucian learned that Senna's soul was trapped in Thresh's lantern.", "994 AN", 994, ERA_REC, 4, [("hecarim", "aggressor"), ("thresh", "aggressor"), ("illaoi", "defender"), ("lucian", "defender"), ("miss-fortune", "defender"), ("olaf", "defender"), ("nagakabouros", "ally"), ("bilgewater", "location")], ["wiki-ruined-king"])
ev("senna-freed", R, "Lucian Frees Senna", "Lucian went to the heart of the Shadow Isles, fought Thresh and freed Senna's soul from the lantern. She came back as a wraith and saved him with a relic cannon.", "995 AN", 995, ERA_REC, 3, [("lucian", "rescuer"), ("senna", "rescued"), ("thresh", "enemy"), ("shadow-isles", "location")], ["wiki-ruined-king", "u-senna"])
ev("annie-awakens-tibbers", R, "Annie Awakens Tibbers", "Annie's grief over her family set off a fire that burned her home. When her guardian tried to tear apart her bear, Annie's rage transformed Tibbers.", "995 AN", 995.5, ERA_REC, 2, [("annie", "protagonist")], ["wiki-recent", "u-annie"])
ev("yasuo-meets-yone", R, "Yasuo Meets Yone", "In Weh'le an azakana demon tried to feed on Yasuo's guilt. A masked swordsman, his brother Yone back from the dead, helped him defeat it, and Yasuo made peace with him.", "996 AN", 996, ERA_REC, 3, [("yasuo", "protagonist"), ("yone", "ally"), ("ionia", "location")], ["wiki-ruined-king", "u-yone"])
ev("syndra-freed", R, "Syndra Breaks Free", "Syndra was freed from her prison at Fae'lor and lifted the ruined castle into the sky. The loss of this Noxian fort pushed Noxus to prepare a second invasion of Ionia.", "996 AN", 996.1, ERA_REC, 3, [("syndra", "protagonist"), ("ionia", "location"), ("noxus", "affected")], ["wiki-recent", "u-syndra"])
ev("kayn-takes-rhaast", R, "Kayn Claims Rhaast", "Kayn of the Order of Shadow took up the Darkin scythe Rhaast and began a struggle for control of his own body.", "996 AN", 996.2, ERA_REC, 3, [("kayn", "wielder"), ("rhaast", "artifact"), ("darkin", "related")], ["wiki-recent", "u-kayn"])
ev("zed-kills-kusho", R, "Zed Kills Master Kusho", "Zed learned that Kusho, now head of the Navori Brotherhood, had freed Jhin. Kusho took the Tears of Shadow and fought, but Zed killed him and, with Kayn's help, took back the Order of Shadow.", "996 AN", 996.3, ERA_REC, 3, [("zed", "victor"), ("kusho", "victim"), ("kayn", "ally"), ("jhin", "pawn")], ["wiki-recent"])
ev("sylas-escapes", R, "Sylas Escapes; the Mage Rebellion", "Sylas used Lux's magic to escape his execution, freed imprisoned mages and charged the palace. His escape started a mage revolt in Demacia.", "996 AN", 996.4, ERA_REC, 5, [("sylas", "instigator"), ("lux", "unwilling aid"), ("garen", "opponent"), ("mageseekers", "enemy"), ("demacia", "location")], ["wiki-mage-rebellion", "u-sylas"])
ev("assassination-of-jarvan-iii", R, "Assassination of King Jarvan III", "Jarvan III tried to calm the crisis by ordering the Mageseekers to stop rounding up mages. An intruder, later revealed as Katarina, killed him in the palace, and Jarvan IV vowed to bring all mages to justice.", "996 AN", 996.5, ERA_REC, 5, [("jarvan-iii", "victim"), ("katarina", "assassin"), ("jarvan-iv", "successor"), ("xin-zhao", "guard")], ["wiki-mage-rebellion", "u-katarina"])
ev("galio-awakens-against-sylas", R, "Galio Answers Lux", "Sylas led Winter's Claw raiders against Garen, Lux and the Demacian army at a northern fortress. As Sylas was about to strike Garen, Lux used her magic to summon Galio, and the army rallied around him.", "997 AN", 997, ERA_REC, 3, [("sylas", "aggressor"), ("winters-claw", "aggressor"), ("lux", "summoner"), ("garen", "defender"), ("galio", "defender")], ["wiki-mage-rebellion"])
ev("defeat-of-the-ruined-king", R, "Defeat of the Ruined King", "Viego, aided by Thresh and Vex, gathered the pieces of Isolde's soul. The Sentinels of Light fought him on the Shadow Isles and in Camavor, and he was defeated and sealed in Alovedra, but Thresh took control of the Black Mist.", "997 AN", 997.1, ERA_REC, 5, [("viego", "antagonist"), ("sentinels-of-light", "victor"), ("lucian", "victor"), ("senna", "victim"), ("gwen", "ally"), ("akshan", "ally"), ("yorick", "ally"), ("vayne", "ally"), ("thresh", "opportunist"), ("camavor", "location")], ["wiki-ruined-king", "wiki-recent"])
ev("kaisa-meets-bel-veth", R, "Kai'Sa Meets Bel'Veth", "After Bel'Veth swallowed a Shuriman port city, Kai'Sa fell into the Lavender Sea and was captured by her. Bel'Veth revealed that Kassadin still lives and demanded that Kai'Sa help her destroy the Watchers.", "997 AN", 997.2, ERA_REC, 4, [("kaisa", "captive"), ("bel-veth", "captor"), ("kassadin", "mentioned"), ("watchers", "target"), ("taliyah", "ally")], ["wiki-recent", "u-belveth"])
ev("ezreal-and-kaisa", R, "Ezreal and Kai'Sa in the Tomb", "Ezreal raided a Shuriman tomb for the Tear of the Goddess and woke voidlings. Kai'Sa stepped in to save him, and they fought the Voidborn together.", "997 AN", 997.3, ERA_REC, 2, [("ezreal", "protagonist"), ("kaisa", "ally"), ("void", "enemy")], ["wiki-recent"])

# --- K/DA events ---
ev("kda-pop-stars", "kda", "K/DA Debuts with 'POP/STARS'", "K/DA was unveiled at the 2018 World Championship opening ceremony in Incheon with an augmented reality performance of 'POP/STARS'. The music video went viral and topped Billboard's World Digital Song Sales chart.", "November 3, 2018", 2018.84, "POP/STARS era", 5, [("kda", "debut"), ("kda-ahri", "performer"), ("kda-akali", "performer"), ("kda-evelynn", "performer"), ("kda-kaisa", "performer")], ["wp-kda", "wp-popstars", "wiki-kda"])
ev("kda-the-baddest", "kda", "Pre-release Single 'THE BADDEST'", "K/DA returned with 'THE BADDEST', the pre-release single for its first EP. It is K/DA Akali's solo song on the record.", "August 27, 2020", 2020.65, "ALL OUT era", 3, [("kda", "artist"), ("kda-akali", "featured")], ["wp-allout", "wp-kda"])
ev("kda-more", "kda", "'MORE' with Seraphine", "The lead single 'MORE' featured all four members plus Seraphine as a guest vocalist. It was the first virtual band song to debut on the Billboard Global 200 and Global Excl. U.S. charts at the same time.", "October 28, 2020", 2020.82, "ALL OUT era", 4, [("kda", "artist"), ("kda-seraphine", "guest"), ("kda-ahri", "performer"), ("kda-akali", "performer"), ("kda-evelynn", "performer"), ("kda-kaisa", "performer")], ["wp-more", "wp-kda"])
ev("kda-all-out", "kda", "ALL OUT EP Released", "K/DA released its five-track debut EP ALL OUT. In the fiction each song was produced by one member, except 'MORE', and Seraphine helped produce the record.", "November 6, 2020", 2020.85, "ALL OUT era", 4, [("kda", "artist"), ("kda-seraphine", "collaborator"), ("kda-ahri", "producer"), ("kda-evelynn", "producer"), ("kda-kaisa", "producer"), ("kda-akali", "producer")], ["wp-allout", "wp-kda", "wiki-kda"])
ev("kda-firestarter", "kda", "Return with FIRESTARTER", "After a long gap, K/DA returned with the title track 'FIRESTARTER' and an EP of the same name. Evelynn and Kai'Sa have new singing voices, and the song 'Girls' features DJ Sona.", "October 18, 2026", 2026.79, "FIRESTARTER era", 4, [("kda", "artist"), ("kda-ahri", "performer"), ("kda-akali", "performer"), ("kda-evelynn", "performer"), ("kda-kaisa", "performer")], ["wp-kda"])

# --- Star Guardian events ---
ev("sg-burning-bright", "star-guardian", "Season 1: Burning Bright", "Empowered by the First Star, high schooler Lux and her team (Janna, Jinx, Lulu and Poppy) secretly protect Valoran City from interstellar monsters while dealing with school drama.", "2016", 2016.0, "Season 1", 4, [("sg-lux", "leader"), ("sg-janna", "mentor"), ("sg-jinx", "member"), ("star-guardians", "subject")], ["wiki-star-guardian"])
ev("sg-a-new-horizon", "star-guardian", "Season 2: A New Horizon", "Veterans Ahri and Miss Fortune return to Valoran City with a rebuilt team after an unknown event destroyed their first squad. They fight alongside Lux's team as Void beasts fall on the city.", "2017", 2017.0, "Season 2", 4, [("sg-ahri", "leader"), ("sg-miss-fortune", "member"), ("sg-lux", "ally"), ("star-guardians", "subject")], ["wiki-star-guardian"])
ev("sg-light-and-shadow", "star-guardian", "Season 3: Light and Shadow", "Ahri's old squad returns, changed by what tore them apart, and brings a threat greater than any before: Zoe, corrupted into the Twilight Star.", "2019", 2019.0, "Season 3", 5, [("sg-zoe", "antagonist"), ("sg-xayah", "fallen guardian"), ("sg-rakan", "fallen guardian"), ("sg-ahri", "protagonist")], ["wiki-star-guardian"])
ev("sg-everything-goes-on", "star-guardian", "Season 4: Everything Goes On", "In a Valoran City scarred by Zoe's invasion, Kai'Sa and Akali lead an untested new team, while a redeemed Xayah leads another. Ancient enemies such as the Star Nemeses rise.", "2022", 2022.0, "Season 4", 4, [("sg-kaisa", "co-leader"), ("sg-akali", "co-leader"), ("sg-xayah", "leader"), ("sg-rakan", "redeemed"), ("star-guardians", "subject")], ["wiki-star-guardian"])

# --- Arcane events (ordered by story; keys use release year with fractions) ---
A1 = "Season 1 (2021)"
A2 = "Season 2 (2024)"
ev("arcane-undercity-uprising", "arcane", "The Failed Undercity Uprising", "Vander led Zaun's people across the bridge against Piltover, and the fighting killed many, including Vi and Powder's parents. Vander gave up fighting and took in the orphaned sisters.", "Before Act 1 (backstory)", 2021.800, A1, 4, [("arcane-vander", "leader"), ("arcane-vi", "orphaned"), ("arcane-jinx", "orphaned"), ("arcane-silco", "participant")], ["wiki-arcane-s1", "wp-arcane"])
ev("arcane-the-heist", "arcane", "The Piltover Heist", "Vi led Powder, Mylo and Claggor in a raid on an inventor's apartment, and a stolen crystal blew up. The workshop belonged to Jayce, who was put on trial for his illegal magic research and expelled from the Academy.", "Act 1, Episode 1 (released November 6, 2021)", 2021.801, A1, 4, [("arcane-vi", "leader"), ("arcane-jinx", "participant"), ("arcane-jayce", "victim"), ("arcane-heimerdinger", "judge"), ("arcane-mel", "councilor")], ["wiki-arcane-s1"])
ev("arcane-vander-captured", "arcane", "Vander Captured by Silco", "Vander surrendered to the enforcers in Vi's place, but Silco's shimmer-boosted thug Deckard killed Benzo and took Vander. Silco revealed the shimmer he had made for a war against Piltover.", "Act 1, Episode 2", 2021.802, A1, 4, [("arcane-silco", "instigator"), ("arcane-vander", "captive"), ("shimmer", "instrument"), ("arcane-singed", "chemist")], ["wiki-arcane-s1"])
ev("arcane-birth-of-hextech", "arcane", "Birth of Hextech", "Viktor helped Jayce stabilize the magic crystals, and in Heimerdinger's lab they made the first working hextech reaction. Councilor Medarda saw it, and Jayce named the new era Hextech.", "Act 1, Episode 3", 2021.803, A1, 5, [("arcane-jayce", "inventor"), ("arcane-viktor", "inventor"), ("arcane-mel", "patron"), ("arcane-heimerdinger", "skeptic"), ("hextech", "created")], ["wiki-arcane-s1", "wp-arcane"])
ev("arcane-powder-becomes-jinx", "arcane", "Powder's Bomb and Silco's Adoption", "Powder's crystal bomb freed Vander from Silco's factory but killed Mylo and Claggor. Vi turned on her and was taken away by Marcus, and Silco, moved by Powder's grief, took her in as his daughter.", "Act 1, Episode 3", 2021.804, A1, 5, [("arcane-jinx", "instigator"), ("arcane-vi", "estranged"), ("arcane-silco", "adoptive father"), ("arcane-vander", "victim"), ("arcane-sevika", "injured"), ("arcane-singed", "injured")], ["wiki-arcane-s1"])
ev("arcane-jayce-joins-council", "arcane", "Jayce Joins the Council", "Years later, after a hextech gemstone theft and a Progress Day crisis, Mel proposed raising Jayce to the Council, and the councilors agreed. Jayce later had Heimerdinger removed from the Council.", "Act 2, Episodes 4–6 (released November 13, 2021)", 2021.830, A1, 4, [("arcane-jayce", "elevated"), ("arcane-mel", "sponsor"), ("arcane-heimerdinger", "removed")], ["wiki-arcane-s1"])
ev("arcane-jinx-kills-silco", "arcane", "The Monster You Created", "Jinx made Vi choose between Powder and Jinx, with Silco and Caitlyn bound at the table. In a panic she killed Silco and then fired a gemstone-powered rocket at the Council chamber as it voted for Zaun's independence.", "Act 3, Episode 9 (released November 20, 2021)", 2021.880, A1, 5, [("arcane-jinx", "instigator"), ("arcane-silco", "victim"), ("arcane-vi", "witness"), ("arcane-caitlyn", "hostage"), ("arcane-jayce", "target")], ["arcwiki-s1e9", "wiki-arcane-s1"])
ev("arcane-council-aftermath", "arcane", "Aftermath of the Council Attack", "The rocket killed several councilors, including Caitlyn's mother. Jayce saved the dying Viktor with the hexcore, and Caitlyn formed an enforcer strike team to hunt Jinx while Ambessa pushed for war.", "Act 1 of Season 2, Episode 1 (released November 9, 2024)", 2024.860, A2, 4, [("arcane-caitlyn", "bereaved"), ("arcane-jayce", "councilor"), ("arcane-viktor", "survivor"), ("arcane-ambessa", "instigator"), ("arcane-vi", "ally")], ["arcwiki-s2e1", "arcwiki-s2"])
ev("arcane-ambessa-black-rose", "arcane", "The Black Rose Strikes at Ambessa", "A Black Rose agent tried to assassinate Ambessa on her flagship, but her bodyguard broke the spell and Ambessa killed her. Ambessa then sped up her plans for Piltover.", "Season 2, Episode 3", 2024.861, A2, 3, [("arcane-ambessa", "target"), ("arcane-leblanc", "instigator")], ["arcwiki-s2e3"])
ev("arcane-warwick-revealed", "arcane", "Vander Lives as Warwick", "Jinx told Vi that Vander was alive, turned by Singed into the beast Warwick. Viktor tried to draw Vander's mind back out of Warwick at his commune, but Ambessa's forces attacked.", "Season 2, Episodes 5–6 (released November 16, 2024)", 2024.870, A2, 4, [("arcane-vander", "transformed"), ("arcane-singed", "creator"), ("arcane-jinx", "ally"), ("arcane-vi", "ally"), ("arcane-viktor", "healer"), ("arcane-ambessa", "aggressor")], ["arcwiki-s2e5", "arcwiki-s2e6"])
ev("arcane-alternate-timeline", "arcane", "Ekko in Another World", "Ekko woke in a timeline where hextech was never invented, Powder never became Jinx, and Piltover and Zaun were at peace. That world's Heimerdinger sacrificed himself to send Ekko home.", "Season 2, Episode 7", 2024.871, A2, 4, [("arcane-ekko", "traveler"), ("arcane-heimerdinger", "sacrifice"), ("arcane-jinx", "alternate self")], ["arcwiki-s2e7"])
ev("arcane-glorious-evolution", "arcane", "Viktor's Glorious Evolution", "Kept alive with Warwick's blood, Viktor woke able to control his followers and named their union the Glorious Evolution. He agreed to change Ambessa's soldiers in return for reaching the anomaly under the hexgates.", "Season 2, Episode 8 (released November 23, 2024)", 2024.890, A2, 5, [("arcane-viktor", "instigator"), ("arcane-singed", "enabler"), ("arcane-ambessa", "ally")], ["arcwiki-s2e8"])
ev("arcane-final-battle", "arcane", "The Battle for Piltover", "Noxus, Piltover and Zaun fought at the hexgate tower, and Mel freed Ambessa from LeBlanc's magic in time to hear her last words. Jayce stayed with Viktor as he undid his Evolution and both vanished into the arcane, while Jinx dragged Warwick off the walkway with her and set off a grenade.", "Season 2, Episode 9 (released November 23, 2024)", 2024.891, A2, 5, [("arcane-jayce", "sacrifice"), ("arcane-viktor", "sacrifice"), ("arcane-jinx", "sacrifice"), ("arcane-vander", "victim"), ("arcane-vi", "survivor"), ("arcane-caitlyn", "combatant"), ("arcane-ambessa", "killed"), ("arcane-mel", "combatant"), ("arcane-leblanc", "combatant"), ("arcane-ekko", "combatant"), ("arcane-sevika", "combatant")], ["arcwiki-s2e9"])
ev("arcane-new-council", "arcane", "A Shared Memorial and a New Council", "Piltover and Zaun held a joint memorial on the bridge, and the reformed Council included Sevika. Mel left for Noxus with her mother's forces, and Caitlyn began to suspect that Jinx survived.", "Season 2, Episode 9 (epilogue)", 2024.892, A2, 3, [("arcane-sevika", "councilor"), ("arcane-mel", "departs"), ("arcane-caitlyn", "investigator"), ("arcane-vi", "survivor")], ["arcwiki-s2e9"])

# ======================= RELATIONSHIPS =======================
rels = []
def rel(s, t, kind, desc, srcs, timeline=None, since=None, until=None):
    rels.append({"source": s, "target": t, "kind": kind, "timeline": timeline, "description": desc,
                 "since_event": since, "until_event": until, "sources": srcs})

# Shurima
rel("nasus", "renekton", "sibling", "Nasus is Renekton's older brother. Renekton saved Old Zuretta until Nasus arrived with relief forces.", ["wiki-golden-age", "u-nasus"])
rel("renekton", "nasus", "enemy", "Driven mad in the tomb, Renekton hunts his brother after his release.", ["wiki-sun-disc", "u-renekton"], R, "tomb-of-the-emperors-opened")
rel("xerath", "renekton", "enemy", "Locked in the tomb with Renekton, Xerath slowly drove him mad.", ["wiki-fall-shurima"], R, "fall-of-shurima")
rel("xerath", "azir", "friend", "Xerath saved young Azir's life and was his trusted servant, hoping Azir would free Shurima's slaves.", ["wiki-fall-shurima"], R, None, "fall-of-shurima")
rel("azir", "xerath", "enemy", "Reborn, Azir learned of Xerath's betrayal and vowed to punish him.", ["wiki-sun-disc", "u-azir"], R, "fall-of-shurima")
rel("sivir", "azir", "family", "Sivir is the last descendant of Azir's bloodline.", ["wiki-sun-disc", "u-sivir"])
rel("azir", "shurima", "leader", "Azir was Shurima's last emperor and has returned to rebuild the empire.", ["u-azir", "wiki-sun-disc"])
rel("cassiopeia", "sivir", "enemy", "Cassiopeia betrayed Sivir in the Tomb of the Emperors.", ["wiki-sun-disc"], R, "tomb-of-the-emperors-opened")
rel("cassiopeia", "katarina", "sibling", "Both are daughters of General Du Couteau of Noxus.", ["u-cassiopeia", "u-katarina"])
rel("cassiopeia", "black-rose", "member", "After her transformation, Cassiopeia used her new form to serve the Black Rose's goals.", ["wiki-sun-disc"])
rel("taliyah", "yasuo", "mentor", "Yasuo took Taliyah as his pupil in Ionia.", ["wiki-sun-disc", "u-taliyah"])
rel("taliyah", "kaisa", "ally", "Taliyah and Kai'Sa traveled together to Xolan.", ["wiki-recent"])
rel("nasus", "ascended", "member", "Nasus is a jackal-headed Ascended.", ["u-nasus"])
rel("renekton", "ascended", "member", "Renekton is an Ascended warrior.", ["u-renekton"])
rel("xerath", "ascended", "member", "Xerath ascended by stealing Azir's ritual.", ["wiki-fall-shurima"], R, "fall-of-shurima")
rel("azir", "ascended", "member", "Azir became an Ascended after saving Sivir.", ["wiki-sun-disc"], R, "rebirth-of-azir")
rel("ascended", "darkin", "variant", "Many Ascended twisted into the Darkin after Shurima fell.", ["wiki-darkin-war"], R, "rise-of-the-darkin")
rel("aurelion-sol", "mount-targon", "enemy", "The Aspects of Targon tricked Aurelion Sol and channeled his power into god-warriors.", ["u-aurelionsol", "wiki-westward"])
rel("jax", "zilean", "ally", "Both are survivors of Icathia: Jax a Kohari guard, Zilean a council member.", ["wiki-void-war", "u-jax"])
rel("jax", "icathia", "member", "Jax was a founding member of the reestablished Kohari, the mage king's guards.", ["wiki-void-war"])
rel("zilean", "icathia", "member", "Zilean sat on Icathia's governing council.", ["u-zilean", "wiki-golden-age"])
rel("malphite", "ixtal", "member", "Malphite is a shard of the Ixtali Monolith.", ["u-malphite", "wiki-void-war"])
rel("skarner", "ixtal", "leader", "Skarner is a founding member of the Yun Tal, Ixtal's ruling caste.", ["u-skarner", "wiki-westward"])
rel("qiyana", "ixtal", "member", "Qiyana is an Ixtali noble who wants the high seat of the Yun Tal.", ["u-qiyana"])
# Void
rel("kassadin", "kaisa", "parent", "Kassadin is Kai'Sa's father, who lost her to the Void.", ["u-kassadin", "wiki-recent"])
rel("kassadin", "malzahar", "enemy", "Kassadin blames the Void prophet Malzahar for losing his family and fights him.", ["wiki-recent", "u-kassadin"])
rel("kaisa", "bel-veth", "enemy", "Bel'Veth captured Kai'Sa and gave her an ultimatum.", ["wiki-recent"], R, "kaisa-meets-bel-veth")
rel("watchers", "bel-veth", "creator", "Bel'Veth calls the Watchers her progenitors and wants to destroy them.", ["wiki-recent"])
rel("watchers", "vel-koz", "creator", "The Watchers made the first Voidborn prototypes, including Vel'Koz.", ["wiki-three-sisters"])
rel("watchers", "void", "leader", "The Watchers are the masters of the Void.", ["u-region-void"])
rel("malzahar", "void", "member", "Malzahar serves the Void as its prophet.", ["u-malzahar"])
rel("kaisa", "ezreal", "ally", "Kai'Sa saved Ezreal from voidlings in a Shuriman tomb.", ["wiki-recent"], R, "ezreal-and-kaisa")
# Darkin
rel("aatrox", "darkin", "member", "Aatrox is one of the Darkin.", ["u-aatrox"])
rel("varus", "darkin", "member", "Varus was the last Darkin sealed in the Great Darkin War.", ["u-varus", "wiki-darkin-war"])
rel("rhaast", "darkin", "member", "Rhaast is a Darkin sealed in a scythe.", ["u-kayn", "wiki-darkin-war"])
rel("kayn", "rhaast", "rival", "Kayn wields Rhaast while each fights for control.", ["u-kayn"], R, "kayn-takes-rhaast")
rel("pantheon", "darkin", "enemy", "The reborn Aspect of War led mortals against the Darkin.", ["wiki-darkin-war"])
rel("zoe", "darkin", "enemy", "Zoe gave Runeterrans the knowledge to seal the Darkin.", ["wiki-darkin-war"])
rel("vladimir", "darkin", "mentor", "A Darkin master taught Vladimir blood magic.", ["wiki-darkin-war"])
# Freljord
rel("lissandra", "avarosa", "sibling", "Lissandra and Avarosa were two of the three Iceborn sisters.", ["wiki-founding-freljord"])
rel("lissandra", "serylda", "sibling", "Lissandra and Serylda were two of the three Iceborn sisters.", ["wiki-founding-freljord"])
rel("avarosa", "serylda", "sibling", "Avarosa and Serylda were sisters who resisted Lissandra together.", ["wiki-three-sisters"])
rel("lissandra", "avarosa", "enemy", "Lissandra sacrificed Avarosa to entomb the Watchers.", ["wiki-three-sisters"], R, "war-of-the-three-sisters")
rel("lissandra", "watchers", "ally", "Lissandra struck a pact with the Watchers, then turned on them and entombed them.", ["wiki-founding-freljord", "wiki-three-sisters"], R, "lissandra-pact-with-watchers", "war-of-the-three-sisters")
rel("lissandra", "frostguard", "leader", "Lissandra secretly leads the Frostguard.", ["u-lissandra"])
rel("volibear", "lissandra", "enemy", "Valhir beat Lissandra in battle and blinded her.", ["wiki-founding-freljord"])
rel("volibear", "ornn", "sibling", "In myth, Valhir and his older brother Ramhaurg fought after Ramhaurg refused to arm the Ursine.", ["wiki-founding-freljord", "u-ornn"])
rel("anivia", "ornn", "sibling", "In Freljordian myth, Anivia is Ramhaurg's sister.", ["wiki-formation"])
rel("ashe", "avarosan", "leader", "Ashe is the warmother of the Avarosans.", ["u-ashe", "wiki-invasion"])
rel("sejuani", "winters-claw", "leader", "Sejuani is the warmother of the Winter's Claw.", ["u-sejuani"])
rel("ashe", "sejuani", "friend", "Ashe and Sejuani became battlesisters in the Winter's Claw.", ["wiki-invasion"], R, None, "ashe-finds-true-ice-bow")
rel("ashe", "sejuani", "rival", "Sejuani branded Ashe a traitor after Ashe protected the Ebrataal tribe.", ["wiki-invasion", "u-sejuani"], R, "ashe-finds-true-ice-bow")
rel("ashe", "avarosa", "other", "Ashe's people believe she is Avarosa reborn.", ["u-ashe"])
rel("sylas", "winters-claw", "ally", "The fleeing Sylas formed an alliance with Winter's Claw raiders.", ["wiki-mage-rebellion"], R, "sylas-escapes")
rel("braum", "freljord", "member", "Braum is a beloved Iceborn hero of the Freljord.", ["u-braum"])
rel("olaf", "freljord", "member", "Olaf is a berserker from Lokfar in the Freljord.", ["u-olaf"])
# Demacia
rel("kayle", "morgana", "sibling", "Kayle and Morgana are twins born to Mihira, host of the Aspect of Justice.", ["wiki-rune-wars", "u-kayle"])
rel("kayle", "morgana", "rival", "The sisters' trust broke and they fought over the city.", ["wiki-resurgence"], R, "winged-sisters-split")
rel("kayle", "demacia", "ally", "Kayle and Morgana protected young Demacia for years.", ["u-kayle", "wiki-resurgence"], R, None, "winged-sisters-split")
rel("garen", "lux", "sibling", "Garen and Lux are siblings of the Crownguard family.", ["u-garen", "u-lux"])
rel("garen", "jarvan-iv", "friend", "Garen met Jarvan IV as a squire and became his friend.", ["wiki-recent", "u-garen"])
rel("jarvan-iii", "jarvan-iv", "parent", "Jarvan III was the king of Demacia and Jarvan IV's father.", ["wiki-mage-rebellion", "u-jarvaniv"])
rel("shyvana", "jarvan-iv", "ally", "Shyvana saved Jarvan IV and serves in his royal guard.", ["u-shyvana", "wiki-mage-rebellion"], R, "shyvana-saves-jarvan")
rel("xin-zhao", "jarvan-iii", "ally", "Xin Zhao served as Jarvan III's personal guard.", ["wiki-invasion", "u-xinzhao"], R, "xin-zhao-joins-demacia", "assassination-of-jarvan-iii")
rel("xin-zhao", "jarvan-iv", "ally", "Jarvan IV asked Xin Zhao to serve as his Seneschal.", ["wiki-mage-rebellion"], R, "assassination-of-jarvan-iii")
rel("katarina", "jarvan-iii", "enemy", "Katarina infiltrated the palace and assassinated Jarvan III.", ["wiki-mage-rebellion"], R, "assassination-of-jarvan-iii")
rel("sylas", "lux", "other", "Sylas manipulated Lux with lessons in controlling her magic and then used her power to escape.", ["wiki-mage-rebellion", "u-sylas"])
rel("sylas", "mageseekers", "enemy", "The Mageseekers imprisoned Sylas as the most dangerous mage in the land.", ["wiki-mage-rebellion", "u-sylas"])
rel("jarvan-iv", "sylas", "enemy", "After his father's death, Jarvan IV vowed to capture all mages.", ["wiki-mage-rebellion"], R, "assassination-of-jarvan-iii")
rel("galio", "lux", "ally", "Lux woke Galio to defend the Demacian army against Sylas.", ["wiki-mage-rebellion"], R, "galio-awakens-against-sylas")
rel("galio", "demacia", "member", "Galio is Demacia's petricite guardian.", ["u-galio"])
rel("poppy", "demacia", "ally", "Poppy keeps Orlon's hammer and searches for the Hero of Demacia.", ["u-poppy", "wiki-resurgence"])
rel("vayne", "evelynn", "enemy", "Vayne hunts the demon who murdered her family.", ["u-vayne", "wiki-recent"], R, "evelynn-kills-vaynes-parents")
rel("sion", "jarvan-i", "enemy", "Sion strangled King Jarvan I in battle.", ["wiki-first-war", "u-sion"], R, "death-of-jarvan-i")
rel("demacia", "noxus", "enemy", "Demacia and Noxus have fought for over a century.", ["wiki-first-war", "wiki-mage-rebellion"], R, "death-of-jarvan-i")
# Noxus
rel("swain", "noxus", "leader", "Swain is the Grand General of Noxus.", ["u-swain"], R, "trifarian-revolution")
rel("boram-darkwill", "noxus", "leader", "Darkwill was the Grand General before Swain's coup.", ["wiki-invasion"], R, None, "trifarian-revolution")
rel("swain", "boram-darkwill", "enemy", "Swain deposed and killed Darkwill.", ["wiki-invasion"], R, "trifarian-revolution")
rel("darius", "draven", "sibling", "Darius and Draven are brothers, orphans from Basilich.", ["wiki-invasion", "u-darius"])
rel("darius", "swain", "ally", "Darius serves Swain as the Hand of Noxus.", ["u-darius", "u-swain"])
rel("draven", "swain", "ally", "Draven helped Swain in his coup.", ["wiki-invasion"], R, "trifarian-revolution")
rel("leblanc", "black-rose", "leader", "LeBlanc is the matron of the Black Rose.", ["wiki-iron-revenant", "u-leblanc"])
rel("vladimir", "black-rose", "member", "Vladimir was there at the Black Rose's founding.", ["wiki-iron-revenant", "u-vladimir"])
rel("leblanc", "vladimir", "ally", "LeBlanc and Vladimir met as equals and founded the Black Rose.", ["wiki-iron-revenant"], R, "founding-of-the-black-rose")
rel("leblanc", "mordekaiser", "enemy", "A LeBlanc from Mordekaiser's own circle helped bring him down.", ["wiki-iron-revenant"], R, "fall-of-mordekaiser")
rel("mordekaiser", "veigar", "enemy", "Mordekaiser imprisoned Veigar in the Immortal Bastion.", ["wiki-iron-revenant", "u-veigar"], R, "veigar-imprisoned")
rel("rell", "black-rose", "enemy", "The Black Rose experimented on Rell, and she escaped and turned against them.", ["u-rell", "wiki-recent"])
rel("riven", "noxus", "member", "Riven was a Noxian swordmaster until the Ionian front broke her faith.", ["u-riven"], R, None, "navori-chemical-attack")
rel("ambessa", "mel", "parent", "Ambessa is Mel's mother and the Medarda matriarch.", ["u-ambessa", "u-mel"])
rel("mel", "leblanc", "other", "Mel found her own magic after an encounter with the Black Rose.", ["u-mel"])
rel("alistar-placeholder", "noxus", "enemy", "", [])  # removed below
rel("singed", "riven", "other", "Riven's warband carried Singed's chemical weapon to Navori.", ["wiki-invasion"], R, "navori-chemical-attack")
# Ionia
rel("irelia", "noxus", "enemy", "Irelia led the Ionian resistance against the Noxian invasion.", ["u-irelia", "wiki-invasion"], R, "noxian-invasion-of-ionia")
rel("irelia", "ionia", "leader", "Irelia was thrust into leading Ionia's resistance and left the role after the war.", ["u-irelia", "wiki-invasion"], R, "noxian-invasion-of-ionia", "battle-of-dalu-bay")
rel("yasuo", "yone", "sibling", "Yone is Yasuo's half-brother.", ["u-yone", "u-yasuo"])
rel("yasuo", "riven", "rival", "Yasuo was blamed for Elder Souma's death, which Riven caused by accident.", ["wiki-ruined-king", "u-yasuo"], R, "navori-chemical-attack")
rel("kusho", "zed", "mentor", "Kusho took Zed as his apprentice.", ["wiki-recent"], R, None, "zed-founds-shadow-order")
rel("kusho", "shen", "mentor", "Kusho led Shen and Zed in the hunt for Jhin.", ["wiki-recent"])
rel("zed", "kusho", "enemy", "Zed killed Kusho after learning he had freed Jhin.", ["wiki-recent"], R, "zed-kills-kusho")
rel("zed", "shen", "rival", "Former fellow students, Zed and Shen became rivals after Zed's banishment.", ["wiki-invasion", "u-zed"], R, "zed-founds-shadow-order")
rel("zed", "shadow-order", "leader", "Zed founded and leads the Order of Shadow.", ["wiki-invasion", "u-zed"], R, "zed-founds-shadow-order")
rel("kayn", "shadow-order", "member", "Kayn is a shadow assassin of the order who hopes to lead it.", ["u-kayn", "wiki-recent"])
rel("zed", "kayn", "mentor", "Kayn is Zed's student and affirmed his loyalty to him.", ["wiki-recent"])
rel("shen", "kinkou-order", "leader", "Shen leads the Kinkou as the Eye of Twilight.", ["u-shen"])
rel("akali", "kinkou-order", "member", "Akali trained as a Kinkou to succeed her mother as Fist of Shadow.", ["wiki-recent", "u-akali"], R, None, "syndra-freed")
rel("shen", "akali", "mentor", "Akali learned from her master Shen.", ["u-akali"])
rel("jhin", "zed", "enemy", "Zed hunted Jhin and later recaptured him in Piltover.", ["wiki-recent", "u-jhin"], R, "capture-of-jhin")
rel("jhin", "shen", "enemy", "Shen helped capture Jhin twice.", ["wiki-recent"], R, "capture-of-jhin")
rel("xayah", "rakan", "romance", "Xayah and Rakan are partners and lovers who fight for their people.", ["u-xayah", "u-rakan"])
rel("ahri", "yasuo", "ally", "Yasuo escorted Ahri on her journey to Bilgewater.", ["wiki-ruined-king", "u-ahri"], R, "yasuo-meets-yone")
rel("ahri", "ionia", "member", "Ahri is a vastaya of Ionia.", ["u-ahri"])
# Shadow Isles / Ruination
rel("viego", "isolde", "romance", "Viego married the seamstress Isolde and was consumed by grief when she died.", ["wiki-ruination", "u-viego"])
rel("isolde", "gwen", "creator", "Isolde, a seamstress, missed someone named Gwen, the doll who later came to life.", ["wiki-ruination", "u-gwen"])
rel("kalista", "viego", "ally", "Kalista served Viego as his general until he betrayed her at Helia.", ["wiki-ruination"], R, None, "the-ruination")
rel("hecarim", "kalista", "enemy", "Hecarim stabbed Kalista in the back during the sack of Helia.", ["wiki-ruination"], R, "the-ruination")
rel("hecarim", "viego", "ally", "Hecarim led Viego's Iron Order in the sack of Helia.", ["wiki-ruination"])
rel("thresh", "viego", "ally", "Erlok Grael guided Viego to the Well of Ages, and Thresh later aided the Ruined King's return.", ["wiki-ruination", "wiki-ruined-king"])
rel("thresh", "senna", "enemy", "Thresh trapped Senna's soul in his lantern.", ["wiki-ruined-king"], R, "death-of-senna", "senna-freed")
rel("lucian", "senna", "romance", "Lucian and Senna are husband and wife.", ["wiki-ruined-king", "u-lucian"])
rel("lucian", "thresh", "enemy", "Lucian hunts Thresh, who killed Senna.", ["u-lucian", "wiki-ruined-king"], R, "death-of-senna")
rel("lucian", "sentinels-of-light", "member", "Lucian is a Sentinel of Light.", ["u-lucian"])
rel("senna", "sentinels-of-light", "member", "Senna joined the Sentinels of Light.", ["u-senna"])
rel("akshan", "sentinels-of-light", "member", "Akshan is a rogue Sentinel who joined the fight against Viego.", ["wiki-ruined-king", "u-akshan"])
rel("vayne", "sentinels-of-light", "member", "Vayne stayed on as the Sentinel of Demacia after Viego's defeat.", ["wiki-ruined-king"], R, "defeat-of-the-ruined-king")
rel("sentinels-of-light", "viego", "enemy", "The Sentinels fought and defeated Viego.", ["wiki-ruined-king"], R, None, "defeat-of-the-ruined-king")
rel("yorick", "sentinels-of-light", "ally", "Yorick helped the Sentinels resist the Mist on the Shadow Isles.", ["wiki-ruined-king"])
rel("tyrus", "ryze", "mentor", "Tyrus was Ryze's master on the Blessed Isles.", ["wiki-ruination", "wiki-rune-wars"], R, None, "ryze-slays-tyrus")
rel("ryze", "tyrus", "enemy", "Ryze killed Tyrus to stop him from using World Runes.", ["wiki-rune-wars"], R, "ryze-slays-tyrus")
rel("ryze", "world-runes", "other", "Ryze hunts the World Runes to keep them hidden.", ["u-ryze", "wiki-rune-wars"], R, "ryze-slays-tyrus")
rel("viego", "camavor", "leader", "Viego was king of Camavor.", ["wiki-ruination", "u-viego"])
# Bilgewater
rel("miss-fortune", "gangplank", "enemy", "Gangplank killed Sarah's parents, and she avenged them by blowing up his flagship.", ["u-missfortune", "wiki-recent"])
rel("illaoi", "nagakabouros", "other", "Illaoi is the Truth Bearer of Nagakabouros.", ["u-illaoi"])
rel("illaoi", "miss-fortune", "ally", "Illaoi worked with Miss Fortune against the Harrowing and the Black Mist.", ["wiki-ruined-king"], R, "harrowing-of-bilgewater")
rel("illaoi", "gangplank", "other", "Illaoi hoped to work with both Miss Fortune and Gangplank to fix Bilgewater.", ["wiki-ruined-king", "u-illaoi"])
rel("graves", "twisted-fate", "friend", "Graves and Twisted Fate are old partners in crime whose bond deepened into romantic feelings.", ["u-graves", "wiki-recent"])
rel("miss-fortune", "bilgewater", "leader", "Miss Fortune took control of most of Bilgewater after Gangplank's fall.", ["wiki-ruined-king"], R, "fall-of-gangplank")
rel("gangplank", "bilgewater", "leader", "Gangplank once ruled Bilgewater as its reaver king.", ["u-gangplank"], R, None, "fall-of-gangplank")
rel("pyke", "bilgewater", "member", "Pyke is a harpooner from Bilgewater's docks.", ["u-pyke"])
# Targon
rel("leona", "diana", "rival", "Leona of the Solari and Diana, host of the moon, are opposed.", ["u-leona", "u-diana"])
rel("leona", "solari", "member", "Leona is a holy warrior of the Solari.", ["u-leona"])
rel("pantheon", "leona", "enemy", "Atreus faced Leona and the Solari at a temple on Mount Targon.", ["wiki-recent"])
rel("zoe", "mount-targon", "member", "Zoe is the Aspect of Twilight and a messenger of Targon.", ["u-zoe"])
# Piltover / Zaun canon
rel("jayce", "viktor", "friend", "Jayce and Viktor met at a Progress Day party and made the first hextech discoveries together.", ["u-jayce"])
rel("jayce", "hextech", "creator", "Jayce and Viktor made the first great hextech discoveries.", ["u-jayce"])
rel("viktor", "hextech", "creator", "Viktor co-created hextech and later embraced the hexcore.", ["u-jayce", "u-viktor"])
rel("caitlyn", "vi", "ally", "Caitlyn and Vi often work as partners.", ["u-caitlyn", "u-vi"])
rel("caitlyn", "jinx", "enemy", "Caitlyn hunts Jinx, the criminal who causes chaos in Piltover.", ["u-caitlyn", "u-jinx"])
rel("singed", "shimmer", "creator", "Singed created shimmer.", ["u-singed"])
rel("janna", "zaun", "ally", "Janna protects the people of Zaun.", ["u-janna", "wiki-resurgence"])
rel("heimerdinger", "piltover", "leader", "Heimerdinger is the longest-serving member of Piltover's council.", ["u-heimerdinger"])
rel("piltover", "zaun", "rival", "Piltover and Zaun were once united but are now separate, interdependent societies.", ["u-region-zaun", "u-region-piltover"])

# ---- variants (AU -> canon) ----
for e in entities:
    if e["variant_of"]:
        rel(e["slug"], e["variant_of"], "variant", e["name"] + " is the " + {"kda": "K/DA", "star-guardian": "Star Guardian", "arcane": "Arcane"}[e["timeline"]] + " version of the canon character.", e["sources"][:1], None)

# ---- K/DA ----
rel("kda-ahri", "kda", "leader", "Ahri founded and leads K/DA.", ["wp-kda"], "kda")
rel("kda-akali", "kda", "member", "Akali is K/DA's main rapper.", ["wp-kda"], "kda")
rel("kda-evelynn", "kda", "member", "Evelynn is one of K/DA's main vocalists.", ["wp-kda"], "kda")
rel("kda-kaisa", "kda", "member", "Kai'Sa is K/DA's main dancer.", ["wp-kda"], "kda")
rel("kda-seraphine", "kda", "ally", "Seraphine collaborated on 'MORE' and helped produce ALL OUT but is not a permanent member.", ["wp-kda", "wp-more"], "kda", "kda-more")
rel("kda-evelynn", "kda-ahri", "friend", "Evelynn reconnected with Ahri to create K/DA.", ["wp-kda"], "kda")
# ---- Star Guardian ----
rel("sg-lux", "star-guardians", "leader", "Lux leads the Season 1 team.", ["wiki-star-guardian"], "star-guardian")
rel("sg-janna", "sg-lux", "mentor", "Janna became Lux's mentor after joining her team.", ["wiki-star-guardian"], "star-guardian")
rel("sg-jinx", "sg-lux", "ally", "Jinx is on Lux's Season 1 team.", ["wiki-star-guardian"], "star-guardian")
rel("sg-ahri", "star-guardians", "leader", "Ahri leads her original, former and current teams.", ["wiki-star-guardian"], "star-guardian")
rel("sg-miss-fortune", "sg-ahri", "ally", "Miss Fortune has served on every one of Ahri's teams.", ["wiki-star-guardian"], "star-guardian")
rel("sg-xayah", "sg-ahri", "ally", "Xayah was on Ahri's original team before she fell.", ["wiki-star-guardian"], "star-guardian", None, "sg-light-and-shadow")
rel("sg-rakan", "sg-ahri", "ally", "Rakan was on Ahri's original team before he fell.", ["wiki-star-guardian"], "star-guardian", None, "sg-light-and-shadow")
rel("sg-zoe", "star-guardians", "enemy", "Corrupted by grief, Zoe became the Twilight Star and invaded Valoran City.", ["wiki-star-guardian"], "star-guardian", "sg-light-and-shadow")
rel("sg-zoe", "sg-xayah", "other", "Xayah, Rakan and Zoe were the corrupted guardians of Season 3.", ["wiki-star-guardian"], "star-guardian", "sg-light-and-shadow", "sg-everything-goes-on")
rel("sg-kaisa", "sg-akali", "ally", "Kai'Sa and Akali co-lead the Season 4 team.", ["wiki-star-guardian"], "star-guardian", "sg-everything-goes-on")
rel("sg-xayah", "sg-rakan", "ally", "Rakan joined Xayah's team after he was healed.", ["wiki-star-guardian"], "star-guardian", "sg-everything-goes-on")
# ---- Arcane ----
rel("arcane-vi", "arcane-jinx", "sibling", "Vi is Powder's older sister.", ["wp-arcane"], "arcane")
rel("arcane-vander", "arcane-vi", "parent", "Vander adopted Vi after her parents died in the uprising.", ["wp-arcane", "wiki-arcane-s1"], "arcane", "arcane-undercity-uprising")
rel("arcane-vander", "arcane-jinx", "parent", "Vander adopted Powder along with Vi.", ["wp-arcane", "wiki-arcane-s1"], "arcane", "arcane-undercity-uprising")
rel("arcane-silco", "arcane-jinx", "parent", "Silco took Powder in and raised her as his daughter.", ["wp-arcane", "wiki-arcane-s1"], "arcane", "arcane-powder-becomes-jinx", "arcane-jinx-kills-silco")
rel("arcane-silco", "arcane-vander", "enemy", "Former brothers-in-arms, they split over Zaun's future, and Silco took Vander captive.", ["wp-arcane", "wiki-arcane-s1"], "arcane", "arcane-vander-captured")
rel("arcane-sevika", "arcane-silco", "ally", "Sevika is Silco's right hand and chief enforcer.", ["wp-arcane", "arcwiki-s1e9"], "arcane")
rel("arcane-jayce", "arcane-viktor", "friend", "Viktor sought Jayce out after his trial, and they became research partners.", ["wiki-arcane-s1", "wp-arcane"], "arcane", "arcane-the-heist")
rel("arcane-heimerdinger", "arcane-jayce", "mentor", "Heimerdinger mentors Jayce.", ["wp-arcane"], "arcane")
rel("arcane-heimerdinger", "arcane-viktor", "mentor", "Viktor was Heimerdinger's assistant.", ["wp-arcane"], "arcane")
rel("arcane-heimerdinger", "arcane-ekko", "mentor", "Heimerdinger later mentors Ekko.", ["wp-arcane"], "arcane")
rel("arcane-caitlyn", "arcane-vi", "romance", "Caitlyn and Vi grow from partners into lovers.", ["wp-arcane", "arcwiki-s2e3"], "arcane")
rel("arcane-mel", "arcane-jayce", "romance", "Mel backs Jayce's work and begins a relationship with him.", ["wp-arcane"], "arcane")
rel("arcane-ambessa", "arcane-mel", "parent", "Ambessa is Mel's mother, who disowned her.", ["wp-arcane"], "arcane")
rel("arcane-singed", "arcane-viktor", "mentor", "Singed was Viktor's former mentor.", ["wp-arcane"], "arcane")
rel("arcane-singed", "arcane-silco", "ally", "Singed was Silco's chief scientist.", ["wp-arcane", "wiki-arcane-s1"], "arcane", None, "arcane-jinx-kills-silco")
rel("arcane-singed", "arcane-ambessa", "ally", "After Silco's death, Singed worked for Ambessa.", ["wp-arcane", "arcwiki-s2e8"], "arcane", "arcane-jinx-kills-silco")
rel("arcane-ekko", "arcane-jinx", "friend", "Ekko was a childhood friend of Vi and Powder.", ["wp-arcane"], "arcane")
rel("arcane-ekko", "firelights", "leader", "Ekko leads the Firelights.", ["wp-arcane"], "arcane")
rel("arcane-ambessa", "arcane-leblanc", "enemy", "Ambessa wants hextech weapons to fight the Black Rose, and LeBlanc's magic trapped her in the final battle.", ["wp-arcane", "arcwiki-s2e3", "arcwiki-s2e9"], "arcane")
rel("arcane-ambessa", "arcane-caitlyn", "mentor", "Ambessa mentored Caitlyn during the occupation of Zaun, then betrayed and stabbed her.", ["arcwiki-s2e8", "arcwiki-s2e9"], "arcane", "arcane-council-aftermath", "arcane-final-battle")
rel("arcane-jinx", "arcane-caitlyn", "enemy", "Jinx's rocket killed Caitlyn's mother, and Caitlyn hunted her.", ["arcwiki-s2e1", "arcwiki-s2e3"], "arcane", "arcane-jinx-kills-silco")
rel("arcane-viktor", "arcane-vander", "other", "Viktor tried to restore Vander's mind from inside Warwick.", ["arcwiki-s2e6"], "arcane", "arcane-warwick-revealed")

# drop placeholder
rels = [r for r in rels if r["source"] != "alistar-placeholder"]

data = {
 "game": {"slug": "league-of-legends", "name": "League of Legends",
          "calendar": "Canon dates use the Noxian calendar, counted from the founding of Noxus (year 0); fans and the wiki write years before it as BN (Before Noxus) and after it as AN (After Noxus), and the exact length of a Noxian year is unknown.",
          "description": "League of Legends is set on Runeterra, a world of rival nations such as Demacia, Noxus, Ionia, Shurima and Piltover and Zaun, shaped by ancient wars between god-warriors, the Darkin, the Void and the cursed Shadow Isles. Riot Games tells the canon (Runeterra Prime) through champion biographies, stories and events, and it also runs alternate skin universes such as K/DA and Star Guardian and the Arcane TV continuity."},
 "wiki": {"base": "https://leagueoflegends.fandom.com/wiki/", "api": "https://leagueoflegends.fandom.com/api.php", "license": "CC BY-SA 3.0 (Fandom; siteinfo reports CC-BY-SA)",
          "notes": "Official JSON works without auth: https://universe-meeps.leagueoflegends.com/v1/en_us/champions/<slug>/index.json returns champion.biography.full/short, title, associated-faction-slug and related-champions (slugs are lowercase with no punctuation, e.g. aurelionsol, belveth, jarvaniv, missfortune). https://universe-meeps.leagueoflegends.com/v1/en_us/search/index.json lists 174 champions and 13 factions. https://universe-meeps.leagueoflegends.com/v1/en_us/factions/<slug>/index.json returns faction.overview.short (e.g. mount-targon, shadow-isles, bandle-city). Non-champion slugs (silco) and guessed skinline paths (skinlines/kda, skinlines/star-guardian) return 403. On the wiki, action=parse&page=<Page>&prop=wikitext&format=json&redirects=1 works; 'Universe:Timeline' does not exist, but 'Timeline' is the hub that links era pages (Creation_of_the_Universe ... Recent_History) and Recent_History links Noxian_Invasion_of_Ionia, Rebirth_of_the_Sun_Disc, Return_of_the_Ruined_King and Great_Mage_Rebellion. AU pages: Riot_Records/KDA, Star_Guardian_(Universe), Arcane_(Universe), Arcane_(TV_Series)/Season_1 (no Season_2 page). Arcane season 2 episode plots came from the Arcane Wiki (arcane.fandom.com/api.php, same API). K/DA release dates came from the Wikipedia query API (prop=extracts)."},
 "sources": sources,
 "timelines": timelines,
 "entities": entities,
 "events": events,
 "relationships": rels,
}

# prune unused sources
used = set()
for coll in (entities, events, rels):
    for x in coll:
        used.update(x["sources"])
data["sources"] = [s for s in sources if s["key"] in used]

with open(OUT, "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("written")
