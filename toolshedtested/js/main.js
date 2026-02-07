// ========================================
// ToolShed Tested - Main JavaScript
// ========================================

// Expanded tool data with real specs, pros/cons, retailer links, and best-for tags
const toolsData = [
    // --- DRILLS & DRIVERS ---
    {
        id: 1,
        name: "DeWalt DCD800 20V MAX XR Drill/Driver",
        category: "drills",
        brand: "dewalt",
        rating: 4.8,
        price: 149.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=DeWalt+DCD800",
        excerpt: "Our top pick — 800 in-lbs of torque in a compact, brushless package. Outstanding battery life and ergonomics.",
        bestFor: "Best Overall",
        dateAdded: "2026-01-15",
        pros: ["Excellent torque-to-weight ratio", "Long battery life", "Compact size fits tight spaces"],
        cons: ["Premium price point", "Batteries sold separately on bare-tool option"],
        specs: { voltage: "20V MAX", torque: "800 in-lbs", speed: "0-650 / 0-2,000 RPM", weight: "3.4 lbs", motor: "Brushless", chuck: '1/2" all-metal ratcheting' },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 2,
        name: "Milwaukee M18 FUEL 2904-22 Hammer Drill",
        category: "drills",
        brand: "milwaukee",
        rating: 4.7,
        price: 179.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Milwaukee+M18+FUEL",
        excerpt: "Powerhouse hammer drill with 1,400 in-lbs of torque. AUTOSTOP control prevents kickback injuries.",
        bestFor: "Best for Pros",
        dateAdded: "2026-01-10",
        pros: ["Massive torque output", "AUTOSTOP kickback control", "One-Key compatible for tool tracking"],
        cons: ["Heavier than competitors", "Overkill for light DIY work"],
        specs: { voltage: "18V", torque: "1,400 in-lbs", speed: "0-550 / 0-2,000 RPM", weight: "4.6 lbs", motor: "POWERSTATE Brushless", chuck: '1/2" all-metal ratcheting' },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 3,
        name: "Ryobi P252 18V ONE+ Drill/Driver",
        category: "drills",
        brand: "ryobi",
        rating: 4.3,
        price: 69.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Ryobi+P252",
        excerpt: "Unbeatable value with the massive ONE+ battery ecosystem. Brushless motor punches above its price.",
        bestFor: "Best Budget",
        dateAdded: "2026-01-20",
        pros: ["Incredible price-to-performance ratio", "ONE+ battery works with 300+ tools", "LED light"],
        cons: ["Less torque than premium options", "Plastic chuck feels less durable"],
        specs: { voltage: "18V ONE+", torque: "515 in-lbs", speed: "0-440 / 0-1,800 RPM", weight: "3.1 lbs", motor: "Brushless", chuck: '1/2" single-sleeve' },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 4,
        name: "Makita XPH14Z 18V LXT Hammer Drill",
        category: "drills",
        brand: "makita",
        rating: 4.6,
        price: 159.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Makita+XPH14Z",
        excerpt: "Precision-engineered with a soft-start feature for delicate work. Star Protection Computer Controls prevent overload.",
        bestFor: "Best for Precision",
        dateAdded: "2026-02-01",
        pros: ["Soft-start prevents bit walking", "Excellent dust and water resistance", "Compact head length"],
        cons: ["Slightly lower torque than Milwaukee", "Battery ecosystem less extensive than some"],
        specs: { voltage: "18V LXT", torque: "1,250 in-lbs", speed: "0-550 / 0-2,100 RPM", weight: "4.4 lbs", motor: "Brushless", chuck: '1/2" all-metal' },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    // --- IMPACT DRIVERS ---
    {
        id: 5,
        name: "DeWalt DCF850B ATOMIC Impact Driver",
        category: "drills",
        brand: "dewalt",
        rating: 4.7,
        price: 119.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=DeWalt+DCF850B",
        excerpt: "Compact powerhouse — only 4.3\" front to back. 3-speed settings let you dial in the right power for every fastener.",
        bestFor: "Best Impact Driver",
        dateAdded: "2026-01-12",
        pros: ["Ultra-compact design", "3-speed selector + precision drive", "1,700 in-lbs of torque"],
        cons: ["No battery included (bare tool)", "Bit holder can be stiff initially"],
        specs: { voltage: "20V MAX", torque: "1,700 in-lbs", speed: "0-1,000 / 0-2,800 / 0-3,250 RPM", weight: "2.1 lbs", motor: "Brushless", drive: '1/4" hex' },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    // --- SAWS ---
    {
        id: 6,
        name: "Milwaukee M18 FUEL Circular Saw 2732-21HD",
        category: "saws",
        brand: "milwaukee",
        rating: 4.9,
        price: 279.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Milwaukee+Circ+Saw",
        excerpt: "Corded-level power in a cordless package. Cuts 2x faster than competitors in our plywood rip tests.",
        bestFor: "Best Circular Saw",
        dateAdded: "2026-01-08",
        pros: ["Corded-equivalent power", "Electronic brake stops blade in under 2 seconds", "Excellent dust blower"],
        cons: ["Heavy with 12.0 battery", "Premium price"],
        specs: { voltage: "18V", blade: '7-1/4"', speed: "5,800 RPM", cutDepth: '2-7/16" at 90deg', weight: "8.0 lbs (bare)", motor: "POWERSTATE Brushless" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 7,
        name: "DeWalt DWS779 12\" Miter Saw",
        category: "saws",
        brand: "dewalt",
        rating: 4.8,
        price: 399.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=DeWalt+Miter+Saw",
        excerpt: "The workshop workhorse. 15-amp motor slices through 4x4s effortlessly. Integrated XPS crosscut alignment system.",
        bestFor: "Best Miter Saw",
        dateAdded: "2026-01-05",
        pros: ["XPS LED crosscut positioning system", "Cuts 2x16 dimensional lumber at 90deg", "Tall sliding fences"],
        cons: ["Heavy at 56 lbs — not very portable", "Dust collection is mediocre"],
        specs: { voltage: "Corded 15A", blade: '12"', speed: "3,800 RPM", bevel: "0-49deg left & right", miter: "0-60deg left / 0-50deg right", weight: "56 lbs" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 8,
        name: "DeWalt DWE7491RS Table Saw",
        category: "saws",
        brand: "dewalt",
        rating: 4.9,
        price: 599.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=DeWalt+Table+Saw",
        excerpt: "The gold standard for jobsite table saws. 32-1/2\" rip capacity handles full plywood sheets. Rolling stand included.",
        bestFor: "Best Table Saw",
        dateAdded: "2025-12-20",
        pros: ['32-1/2" rip capacity', "Rolling stand for easy transport", "Rack and pinion telescoping fence"],
        cons: ["Dust collection port clogs frequently", "No dado capability out of the box"],
        specs: { voltage: "Corded 15A", blade: '10"', speed: "4,800 RPM", ripCapacity: '32-1/2"', weight: "110 lbs (with stand)", table: '26-1/4" x 22"' },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 9,
        name: "Bosch JS572EBK Jigsaw",
        category: "saws",
        brand: "bosch",
        rating: 4.6,
        price: 179.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Bosch+Jigsaw",
        excerpt: "Toolless blade changes and constant-response circuitry for consistent cuts under load. Best in class for curves.",
        bestFor: "Best Jigsaw",
        dateAdded: "2026-01-18",
        pros: ["Toolless blade change system", "Very low vibration", "Excellent orbital action for fast cuts"],
        cons: ["Dust blower is weak", "Corded only — no battery option"],
        specs: { voltage: "Corded 7.2A", stroke: '1"', speed: "500-3,100 SPM", bevels: "0-45deg both directions", weight: "4.8 lbs", bladeChange: "Toolless T-shank" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 10,
        name: "Milwaukee 2821-21 M18 FUEL SAWZALL",
        category: "saws",
        brand: "milwaukee",
        rating: 4.7,
        price: 249.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Milwaukee+SAWZALL",
        excerpt: "50% faster than competitors in our demolition tests. Fixtec blade clamp allows one-handed blade changes.",
        bestFor: "Best Reciprocating Saw",
        dateAdded: "2026-01-22",
        pros: ["Fastest cutting speed we tested", "One-handed blade changes", "Orbital action for aggressive cuts"],
        cons: ["Vibration can fatigue hands on long jobs", "Battery drains fast under heavy load"],
        specs: { voltage: "18V", stroke: '1-1/4"', speed: "0-3,000 SPM", weight: "7.5 lbs", motor: "POWERSTATE Brushless", bladeChange: "FIXTEC one-handed" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    // --- GRINDERS ---
    {
        id: 11,
        name: "Makita XAG04Z 18V Angle Grinder",
        category: "grinders",
        brand: "makita",
        rating: 4.6,
        price: 119.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Makita+Grinder",
        excerpt: "Automatic Speed Change technology adjusts speed and torque under load. Electric brake stops disc in 2 seconds.",
        bestFor: "Best Angle Grinder",
        dateAdded: "2026-01-14",
        pros: ["Auto speed change under load", "Electric brake for safety", "Rubberized soft grip"],
        cons: ["Guard adjustment is stiff", "Side handle only has one mounting position"],
        specs: { voltage: "18V LXT", disc: '4-1/2" / 5"', speed: "8,500 RPM", weight: "5.1 lbs", motor: "Brushless", spindle: "5/8-11 UNC" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 12,
        name: "DeWalt DCG413B 20V Angle Grinder",
        category: "grinders",
        brand: "dewalt",
        rating: 4.5,
        price: 139.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=DeWalt+Grinder",
        excerpt: "Brake engages when paddle switch is released, stopping wheel in 2 seconds. Kickback brake for added safety.",
        bestFor: "Safest Grinder",
        dateAdded: "2026-01-16",
        pros: ["Dual safety braking system", "Mesh intake screen blocks debris", "E-Clutch prevents kickback injuries"],
        cons: ["Switch can be accidentally activated", "Shorter runtime than Makita"],
        specs: { voltage: "20V MAX", disc: '4-1/2" / 5"', speed: "9,000 RPM", weight: "4.5 lbs", motor: "Brushless", spindle: "5/8-11 UNC" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    // --- SANDERS ---
    {
        id: 13,
        name: "Bosch ROS20VSC Random Orbit Sander",
        category: "sanders",
        brand: "bosch",
        rating: 4.7,
        price: 79.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Bosch+Sander",
        excerpt: "Variable speed control with microfilter dust canister. Produces the smoothest, most swirl-free finishes we tested.",
        bestFor: "Best Orbital Sander",
        dateAdded: "2026-01-25",
        pros: ["Best dust collection in class", "No swirl marks at any speed", "Soft-grip top and body"],
        cons: ["Corded only", "Pad brake sometimes leaves marks on soft wood"],
        specs: { voltage: "Corded 2.5A", pad: '5"', speed: "7,500-12,000 OPM", dustCollection: "Microfilter canister", weight: "3.5 lbs", orbit: "Random" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 14,
        name: "Makita XOB01Z 18V Random Orbit Sander",
        category: "sanders",
        brand: "makita",
        rating: 4.5,
        price: 99.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Makita+ROS",
        excerpt: "Cordless freedom without sacrificing power. 3-speed selector for finesse to aggressive material removal.",
        bestFor: "Best Cordless Sander",
        dateAdded: "2026-01-28",
        pros: ["Cordless convenience", "3-speed settings", "Low vibration at all speeds"],
        cons: ["Dust collection bag is small", "Not as powerful as corded options for heavy stock removal"],
        specs: { voltage: "18V LXT", pad: '5"', speed: "7,000 / 9,500 / 11,000 OPM", dustCollection: "Dust bag", weight: "3.3 lbs (bare)", orbit: "Random" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    // --- OUTDOOR POWER EQUIPMENT ---
    {
        id: 15,
        name: "DeWalt DCCS670X1 60V Chainsaw",
        category: "outdoor",
        brand: "dewalt",
        rating: 4.6,
        price: 299.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=DeWalt+Chainsaw",
        excerpt: "Battery-powered chainsaw that rivals gas performance. Low kickback 16\" Oregon bar and chain.",
        bestFor: "Best Battery Chainsaw",
        dateAdded: "2026-01-30",
        pros: ["No gas, no fumes, no pull-start", "Low kickback bar and chain", "Tool-free chain tensioning"],
        cons: ["Runtime limited to ~70 cuts on 4x4", "60V battery is expensive to replace"],
        specs: { voltage: "60V MAX FLEXVOLT", bar: '16"', speed: "26.2 ft/s chain speed", weight: "12.2 lbs (with battery)", oilCapacity: "4.4 oz", chainType: "Oregon low-kickback" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 16,
        name: "Milwaukee M18 FUEL String Trimmer 2828-21ST",
        category: "outdoor",
        brand: "milwaukee",
        rating: 4.5,
        price: 219.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Milwaukee+Trimmer",
        excerpt: "Variable speed trigger and Easy Load trimmer head make this the easiest cordless trimmer we've used.",
        bestFor: "Best String Trimmer",
        dateAdded: "2026-02-03",
        pros: ["Easy Load trimmer head (no dis-assembly)", "Variable speed trigger", "QUIK-LOK attachment system"],
        cons: ["Heavier than gas equivalents", "Battery not included in some kits"],
        specs: { voltage: "18V", cuttingSwath: '16"', speed: "5,800 RPM", weight: "10.5 lbs (bare)", lineType: "0.080 / 0.095 dual line", attachment: "QUIK-LOK compatible" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 17,
        name: "Ryobi RY401150US 40V Lawn Mower",
        category: "outdoor",
        brand: "ryobi",
        rating: 4.4,
        price: 349.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Ryobi+Mower",
        excerpt: "Self-propelled and whisper-quiet. Handles a 1/3-acre lot on a single charge. Our best-value mower pick.",
        bestFor: "Best Battery Mower",
        dateAdded: "2026-02-05",
        pros: ["Self-propelled rear-wheel drive", "Quieter than gas mowers", "Handles 1/3-acre on one charge"],
        cons: ["Mulching capability is average", "Plastic deck won't last as long as steel"],
        specs: { voltage: "40V", deckWidth: '21"', height: '1.5"-4"', weight: "57 lbs", driveType: "Self-propelled rear-wheel", runtime: "45 min (6.0 Ah battery)" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 18,
        name: "EGO LB6504 56V Leaf Blower",
        category: "outdoor",
        brand: "other",
        rating: 4.7,
        price: 249.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=EGO+Blower",
        excerpt: "Hurricane-force 650 CFM airflow. The most powerful cordless blower we've ever tested — rivals gas backpack models.",
        bestFor: "Most Powerful Blower",
        dateAdded: "2026-01-27",
        pros: ["650 CFM / 180 MPH — gas-level power", "Turbo button for wet leaves", "Variable speed dial"],
        cons: ["Loud at max power", "Heavy with 5.0 Ah battery"],
        specs: { voltage: "56V ARC Lithium", airflow: "650 CFM", airSpeed: "180 MPH", weight: "9.6 lbs (with battery)", runtime: "Up to 75 min (low)", noise: "65 dB (low speed)" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    // --- MULTI-TOOLS / SPECIALTY ---
    {
        id: 19,
        name: "Milwaukee M18 FUEL Multi-Tool 2836-20",
        category: "grinders",
        brand: "milwaukee",
        rating: 4.6,
        price: 159.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Milwaukee+Multi-Tool",
        excerpt: "OPEN-LOK blade changes are genuinely one-handed. Fastest oscillating tool blade change system on the market.",
        bestFor: "Best Multi-Tool",
        dateAdded: "2026-02-01",
        pros: ["OPEN-LOK one-handed blade change", "Variable speed 11,000-20,000 OPM", "Constant power technology"],
        cons: ["Vibration is higher than Bosch StarlockMax", "Blades are proprietary to OPEN-LOK"],
        specs: { voltage: "18V", speed: "11,000-20,000 OPM", oscillation: "3.6deg", weight: "3.99 lbs", bladeSystem: "OPEN-LOK + Universal", motor: "POWERSTATE Brushless" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 20,
        name: "Bosch GOP18V-28N StarlockMax Multi-Tool",
        category: "grinders",
        brand: "bosch",
        rating: 4.5,
        price: 139.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Bosch+Multi-Tool",
        excerpt: "Lowest vibration oscillating tool we tested. StarlockMax 3D blade mount provides strongest blade grip available.",
        bestFor: "Lowest Vibration",
        dateAdded: "2026-01-19",
        pros: ["Lowest vibration in class", "StarlockMax is the strongest blade mount", "EC Brushless motor is very efficient"],
        cons: ["StarlockMax blades are expensive", "Less common in stores than Milwaukee blades"],
        specs: { voltage: "18V", speed: "8,000-20,000 OPM", oscillation: "3.2deg", weight: "3.5 lbs", bladeSystem: "Starlock / StarlockPlus / StarlockMax", motor: "EC Brushless" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    // --- ROUTERS & SPECIALTY ---
    {
        id: 21,
        name: "DeWalt DWP611PK Compact Router",
        category: "sanders",
        brand: "dewalt",
        rating: 4.8,
        price: 199.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=DeWalt+Router",
        excerpt: "The compact router that started a revolution. Dual-base system (fixed + plunge) at a price that's hard to beat.",
        bestFor: "Best Compact Router",
        dateAdded: "2026-01-11",
        pros: ["Fixed + plunge base included", "Soft-start and variable speed", "Dual LED headlights"],
        cons: ["Dust collection requires separate adapter", "Collet is 1/4\" only (no 1/2\")"],
        specs: { voltage: "Corded 7A (1.25 HP)", collet: '1/4"', speed: "16,000-27,000 RPM", bases: "Fixed + Plunge included", weight: "4.0 lbs (fixed base)", plungeDepth: '1-1/2"' },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 22,
        name: "Makita BO5041K Random Orbit Sander",
        category: "sanders",
        brand: "makita",
        rating: 4.4,
        price: 69.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Makita+BO5041K",
        excerpt: "Variable speed with pad control for consistent finishes. Cloth dust bag collects 90%+ of sanding debris.",
        bestFor: "Best Value Sander",
        dateAdded: "2026-01-29",
        pros: ["Excellent dust collection", "Pad control prevents spinning on lift-off", "Very affordable"],
        cons: ["Corded only", "Vibration higher than Bosch ROS20VSC"],
        specs: { voltage: "Corded 3A", pad: '5"', speed: "4,000-12,000 OPM", dustCollection: "Cloth bag + vacuum port", weight: "2.9 lbs", orbit: "Random" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    // --- WELDERS ---
    {
        id: 23,
        name: "Hobart Handler 210 MVP MIG Welder",
        category: "welders",
        brand: "other",
        rating: 4.7,
        price: 999.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=Hobart+210+MVP",
        excerpt: "Multi-voltage plug (MVP) runs on 115V or 230V. Welds up to 3/8\" steel. Our top pick for serious home welders.",
        bestFor: "Best MIG Welder",
        dateAdded: "2026-01-06",
        pros: ["Runs on 115V or 230V power", "Welds up to 3/8\" steel", "5-position voltage selector is easy to set"],
        cons: ["Heavy at 79 lbs", "Wire feed speed dial lacks fine calibration"],
        specs: { inputVoltage: "115V / 230V (MVP)", ampRange: "25-210A", dutyCycle: "30% at 150A", wireSize: "0.024-0.045 MIG", weight: "79 lbs", processes: "MIG / Flux-core" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    },
    {
        id: 24,
        name: "YesWelder MIG-205DS Multi-Process Welder",
        category: "welders",
        brand: "other",
        rating: 4.3,
        price: 389.00,
        image: "https://placehold.co/400x300/1a1a1a/ff6b00?text=YesWelder+205DS",
        excerpt: "MIG, TIG, and Stick in one machine at a budget price. Synergic controls make setup beginner-friendly.",
        bestFor: "Best Budget Welder",
        dateAdded: "2026-01-09",
        pros: ["3-in-1: MIG, TIG, Stick", "Synergic one-knob setup", "Incredibly affordable"],
        cons: ["TIG is lift-arc only (no HF start)", "Build quality is a step below Hobart/Lincoln"],
        specs: { inputVoltage: "110V / 220V", ampRange: "30-205A", dutyCycle: "60% at 160A", processes: "MIG / TIG / Stick / Flux-core", wireSize: "0.023-0.035 MIG", weight: "30 lbs" },
        retailers: { amazon: "#", homeDepot: "#", lowes: "#" }
    }
];

// Category definitions with descriptions
const categoryData = {
    drills: { label: "Drills & Drivers", icon: "drill", count: 5 },
    saws: { label: "Saws", icon: "saw", count: 5 },
    grinders: { label: "Grinders & Multi-Tools", icon: "grinder", count: 4 },
    sanders: { label: "Sanders & Routers", icon: "sander", count: 4 },
    outdoor: { label: "Outdoor Power", icon: "outdoor", count: 4 },
    welders: { label: "Welders", icon: "welder", count: 2 }
};

// ========================================
// Theme Management
// ========================================
class ThemeManager {
    constructor() {
        this.themeToggle = document.querySelector('.theme-toggle');
        this.currentTheme = localStorage.getItem('theme') || 'dark';
        this.init();
    }

    init() {
        this.setTheme(this.currentTheme);
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => this.toggleTheme());
        }
    }

    setTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;
    }

    toggleTheme() {
        const newTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.setTheme(newTheme);
    }
}

// ========================================
// Mobile Menu
// ========================================
class MobileMenu {
    constructor() {
        this.toggle = document.querySelector('.mobile-menu-toggle');
        this.menu = document.querySelector('.nav-menu');
        this.init();
    }

    init() {
        if (!this.toggle || !this.menu) return;

        this.toggle.addEventListener('click', () => this.toggleMenu());

        document.addEventListener('click', (e) => {
            if (!this.toggle.contains(e.target) && !this.menu.contains(e.target)) {
                this.closeMenu();
            }
        });

        const menuLinks = this.menu.querySelectorAll('a');
        menuLinks.forEach(link => {
            link.addEventListener('click', () => this.closeMenu());
        });
    }

    toggleMenu() {
        const isExpanded = this.toggle.getAttribute('aria-expanded') === 'true';
        this.toggle.setAttribute('aria-expanded', !isExpanded);
        this.menu.classList.toggle('active');
    }

    closeMenu() {
        this.toggle.setAttribute('aria-expanded', 'false');
        this.menu.classList.remove('active');
    }
}

// ========================================
// Dropdown Navigation
// ========================================
class DropdownNav {
    constructor() {
        this.dropdowns = document.querySelectorAll('.nav-dropdown');
        this.init();
    }

    init() {
        this.dropdowns.forEach(dropdown => {
            const trigger = dropdown.querySelector('.nav-dropdown-trigger');
            const menu = dropdown.querySelector('.nav-dropdown-menu');
            if (!trigger || !menu) return;

            // Keyboard support
            trigger.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    dropdown.classList.toggle('open');
                }
                if (e.key === 'Escape') {
                    dropdown.classList.remove('open');
                    trigger.focus();
                }
            });

            // Close on click outside
            document.addEventListener('click', (e) => {
                if (!dropdown.contains(e.target)) {
                    dropdown.classList.remove('open');
                }
            });
        });
    }
}

// ========================================
// Search Functionality
// ========================================
class SearchManager {
    constructor(data) {
        this.data = data;
        this.searchInput = document.getElementById('site-search');
        this.searchResults = document.getElementById('search-results');
        this.searchButton = document.querySelector('.search-button');
        this.debounceTimer = null;
        this.init();
    }

    init() {
        if (!this.searchInput) return;

        this.searchInput.addEventListener('input', (e) => {
            clearTimeout(this.debounceTimer);
            this.debounceTimer = setTimeout(() => this.performSearch(e.target.value), 300);
        });

        if (this.searchButton) {
            this.searchButton.addEventListener('click', () => {
                this.performSearch(this.searchInput.value);
            });
        }

        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.performSearch(this.searchInput.value);
            }
        });

        document.addEventListener('click', (e) => {
            if (!this.searchInput.contains(e.target) && !this.searchResults.contains(e.target)) {
                this.hideResults();
            }
        });
    }

    performSearch(query) {
        if (!query || query.length < 2) {
            this.hideResults();
            return;
        }

        const results = this.data.filter(tool => {
            const searchText = query.toLowerCase();
            return (
                tool.name.toLowerCase().includes(searchText) ||
                tool.category.toLowerCase().includes(searchText) ||
                tool.brand.toLowerCase().includes(searchText) ||
                tool.excerpt.toLowerCase().includes(searchText) ||
                (tool.bestFor && tool.bestFor.toLowerCase().includes(searchText))
            );
        });

        this.displayResults(results, query);
    }

    displayResults(results, query) {
        if (results.length === 0) {
            this.searchResults.innerHTML = `
                <div class="search-result-item">
                    <p style="text-align: center; color: var(--text-tertiary);">
                        No results found for "${this.escapeHtml(query)}"
                    </p>
                </div>
            `;
            this.searchResults.classList.add('active');
            return;
        }

        this.searchResults.innerHTML = results.map(tool => `
            <div class="search-result-item" role="option" tabindex="0" data-tool-id="${tool.id}">
                <div style="display: flex; gap: 1rem; align-items: center;">
                    <img src="${tool.image}" alt="${this.escapeHtml(tool.name)}"
                         style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;"
                         loading="lazy">
                    <div>
                        <strong>${this.escapeHtml(tool.name)}</strong>
                        ${tool.bestFor ? `<span class="search-badge">${this.escapeHtml(tool.bestFor)}</span>` : ''}
                        <div style="display: flex; gap: 1rem; margin-top: 0.25rem; font-size: 0.875rem; color: var(--text-secondary);">
                            <span>${this.escapeHtml(categoryData[tool.category]?.label || tool.category)}</span>
                            <span>${this.generateStars(tool.rating)} ${tool.rating}</span>
                            <span>$${tool.price}</span>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        this.searchResults.classList.add('active');

        this.searchResults.querySelectorAll('.search-result-item').forEach((item) => {
            item.addEventListener('click', () => {
                const toolId = item.dataset.toolId;
                const tool = this.data.find(t => t.id == toolId);
                if (tool) this.selectResult(tool);
            });
        });
    }

    selectResult(tool) {
        this.hideResults();
        this.searchInput.value = '';
        // Scroll to reviews and filter
        const reviewsSection = document.getElementById('reviews');
        if (reviewsSection) {
            reviewsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    hideResults() {
        this.searchResults.classList.remove('active');
    }

    generateStars(rating) {
        const full = Math.floor(rating);
        const half = rating % 1 >= 0.5 ? 1 : 0;
        return '\u2605'.repeat(full) + (half ? '\u2606' : '') + '\u2606'.repeat(5 - full - half);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// ========================================
// Reviews Manager
// ========================================
class ReviewsManager {
    constructor(data) {
        this.data = data;
        this.reviewsGrid = document.getElementById('reviews-grid');
        this.loadMoreBtn = document.getElementById('load-more');
        this.displayedCount = 6;
        this.filteredData = [...data];
        this.init();
    }

    init() {
        if (!this.reviewsGrid) return;

        this.renderReviews();

        if (this.loadMoreBtn) {
            this.loadMoreBtn.addEventListener('click', () => this.loadMore());
        }

        this.setupFilters();
    }

    setupFilters() {
        const categoryFilter = document.getElementById('category-filter');
        const sortFilter = document.getElementById('sort-filter');
        const brandFilter = document.getElementById('brand-filter');

        [categoryFilter, sortFilter, brandFilter].forEach(filter => {
            if (filter) {
                filter.addEventListener('change', () => this.applyFilters());
            }
        });
    }

    applyFilters() {
        const category = document.getElementById('category-filter')?.value || 'all';
        const sort = document.getElementById('sort-filter')?.value || 'rating';
        const brand = document.getElementById('brand-filter')?.value || 'all';

        this.filteredData = this.data.filter(tool => {
            const categoryMatch = category === 'all' || tool.category === category;
            const brandMatch = brand === 'all' || tool.brand === brand;
            return categoryMatch && brandMatch;
        });

        switch (sort) {
            case 'rating':
                this.filteredData.sort((a, b) => b.rating - a.rating);
                break;
            case 'recent':
                this.filteredData.sort((a, b) => new Date(b.dateAdded) - new Date(a.dateAdded));
                break;
            case 'popular':
                this.filteredData.sort((a, b) => b.rating - a.rating);
                break;
            case 'price-low':
                this.filteredData.sort((a, b) => a.price - b.price);
                break;
            case 'price-high':
                this.filteredData.sort((a, b) => b.price - a.price);
                break;
        }

        this.displayedCount = 6;
        this.renderReviews();

        // Update breadcrumbs
        const breadcrumbManager = window.breadcrumbManagerInstance;
        if (breadcrumbManager) {
            breadcrumbManager.updateBreadcrumbs(category);
        }
    }

    renderReviews() {
        const reviewsToShow = this.filteredData.slice(0, this.displayedCount);

        if (reviewsToShow.length === 0) {
            this.reviewsGrid.innerHTML = `
                <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-tertiary);">
                    <p style="font-size: 1.25rem;">No tools match your filters.</p>
                    <p>Try adjusting your category or brand selection.</p>
                </div>
            `;
            if (this.loadMoreBtn) this.loadMoreBtn.style.display = 'none';
            return;
        }

        this.reviewsGrid.innerHTML = reviewsToShow.map(tool => `
            <article class="review-card" data-category="${tool.category}">
                <div class="review-image-wrapper">
                    <img src="${tool.image}" alt="${tool.name} - reviewed and tested" class="review-image" loading="lazy" width="400" height="300">
                    ${tool.bestFor ? `<span class="review-badge">${tool.bestFor}</span>` : ''}
                </div>
                <div class="review-content">
                    <span class="review-category">${categoryData[tool.category]?.label || tool.category}</span>
                    <h3 class="review-title">${tool.name}</h3>
                    <div class="review-rating">
                        <span class="stars">${this.generateStars(tool.rating)}</span>
                        <span class="rating-number">${tool.rating}/5</span>
                    </div>
                    <p class="review-excerpt">${tool.excerpt}</p>
                    ${this.renderProsConsCompact(tool)}
                    <div class="review-meta">
                        <span class="review-price">$${tool.price.toFixed(2)}</span>
                        <div class="review-retailers">
                            ${tool.retailers?.amazon ? '<a href="#" class="retailer-link" title="Check price on Amazon">Amazon</a>' : ''}
                            ${tool.retailers?.homeDepot ? '<a href="#" class="retailer-link" title="Check price on Home Depot">Home Depot</a>' : ''}
                            ${tool.retailers?.lowes ? '<a href="#" class="retailer-link" title="Check price on Lowe\'s">Lowe\'s</a>' : ''}
                        </div>
                    </div>
                </div>
            </article>
        `).join('');

        if (this.loadMoreBtn) {
            this.loadMoreBtn.style.display =
                this.displayedCount >= this.filteredData.length ? 'none' : 'block';
        }
    }

    renderProsConsCompact(tool) {
        if (!tool.pros || !tool.cons) return '';
        return `
            <div class="review-pros-cons">
                <div class="pros-compact">
                    <span class="pros-icon">+</span>
                    <span>${tool.pros[0]}</span>
                </div>
                <div class="cons-compact">
                    <span class="cons-icon">-</span>
                    <span>${tool.cons[0]}</span>
                </div>
            </div>
        `;
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        let stars = '\u2605'.repeat(fullStars);
        if (hasHalfStar) stars += '\u2606';
        const emptyStars = 5 - Math.ceil(rating);
        stars += '\u2606'.repeat(emptyStars);
        return stars;
    }

    loadMore() {
        this.displayedCount += 6;
        this.renderReviews();
    }
}

// ========================================
// Tool Comparison (enhanced with winner highlighting)
// ========================================
class ComparisonManager {
    constructor(data) {
        this.data = data;
        this.compareSelects = document.querySelectorAll('.compare-select');
        this.comparisonResults = document.getElementById('comparison-results');
        this.selectedTools = [null, null, null];
        this.init();
    }

    init() {
        if (!this.comparisonResults) return;

        this.populateSelects();

        this.compareSelects.forEach((select, index) => {
            select.addEventListener('change', (e) => {
                this.handleSelection(index, e.target.value);
            });
        });
    }

    populateSelects() {
        // Group by category
        const grouped = {};
        this.data.forEach(tool => {
            const catLabel = categoryData[tool.category]?.label || tool.category;
            if (!grouped[catLabel]) grouped[catLabel] = [];
            grouped[catLabel].push(tool);
        });

        let optionsHtml = '<option value="">Select a tool...</option>';
        for (const [cat, tools] of Object.entries(grouped)) {
            optionsHtml += `<optgroup label="${cat}">`;
            tools.forEach(tool => {
                optionsHtml += `<option value="${tool.id}">${tool.name} — $${tool.price}</option>`;
            });
            optionsHtml += '</optgroup>';
        }

        this.compareSelects.forEach(select => {
            const currentValue = select.value;
            select.innerHTML = optionsHtml;
            select.value = currentValue;
        });
    }

    handleSelection(index, toolId) {
        if (toolId) {
            this.selectedTools[index] = this.data.find(t => t.id == toolId);
        } else {
            this.selectedTools[index] = null;
        }
        this.renderComparison();
    }

    renderComparison() {
        const validTools = this.selectedTools.filter(t => t !== null);

        if (validTools.length === 0) {
            this.comparisonResults.innerHTML = '<p class="comparison-placeholder">Select tools above to begin comparing</p>';
            return;
        }

        // Find best rating and lowest price for highlighting
        const bestRating = Math.max(...validTools.map(t => t.rating));
        const lowestPrice = Math.min(...validTools.map(t => t.price));

        const html = `
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Specification</th>
                        ${validTools.map(tool => `<th>
                            ${tool.name}
                            ${tool.bestFor ? `<br><small style="color: var(--accent-primary);">${tool.bestFor}</small>` : ''}
                        </th>`).join('')}
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Rating</strong></td>
                        ${validTools.map(tool => `<td class="${tool.rating === bestRating && validTools.length > 1 ? 'winner-cell' : ''}">
                            ${this.generateStars(tool.rating)} ${tool.rating}/5
                            ${tool.rating === bestRating && validTools.length > 1 ? ' <span class="winner-badge">BEST</span>' : ''}
                        </td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Price</strong></td>
                        ${validTools.map(tool => `<td class="${tool.price === lowestPrice && validTools.length > 1 ? 'winner-cell' : ''}" style="font-weight: 700; color: var(--accent-primary);">
                            $${tool.price.toFixed(2)}
                            ${tool.price === lowestPrice && validTools.length > 1 ? ' <span class="winner-badge">LOWEST</span>' : ''}
                        </td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Category</strong></td>
                        ${validTools.map(tool => `<td>${categoryData[tool.category]?.label || tool.category}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Brand</strong></td>
                        ${validTools.map(tool => `<td>${tool.brand.charAt(0).toUpperCase() + tool.brand.slice(1)}</td>`).join('')}
                    </tr>
                    ${this.renderSpecs(validTools)}
                    <tr>
                        <td><strong>Top Pro</strong></td>
                        ${validTools.map(tool => `<td style="color: var(--success-color);">${tool.pros ? tool.pros[0] : 'N/A'}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Top Con</strong></td>
                        ${validTools.map(tool => `<td style="color: var(--error-color);">${tool.cons ? tool.cons[0] : 'N/A'}</td>`).join('')}
                    </tr>
                    <tr>
                        <td><strong>Buy</strong></td>
                        ${validTools.map(tool => `<td>
                            <a href="#" class="btn btn-primary btn-small" style="display: inline-block; margin: 2px;">Amazon</a>
                            <a href="#" class="btn btn-secondary btn-small" style="display: inline-block; margin: 2px; padding: 4px 8px;">HD</a>
                        </td>`).join('')}
                    </tr>
                </tbody>
            </table>
        `;

        this.comparisonResults.innerHTML = html;
    }

    renderSpecs(tools) {
        const allSpecs = new Set();
        tools.forEach(tool => {
            if (tool.specs) Object.keys(tool.specs).forEach(key => allSpecs.add(key));
        });

        return Array.from(allSpecs).map(spec => `
            <tr>
                <td><strong>${this.formatSpecName(spec)}</strong></td>
                ${tools.map(tool => `<td>${(tool.specs && tool.specs[spec]) || 'N/A'}</td>`).join('')}
            </tr>
        `).join('');
    }

    formatSpecName(spec) {
        return spec
            .replace(/([A-Z])/g, ' $1')
            .replace(/^./, str => str.toUpperCase())
            .trim();
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        return '\u2605'.repeat(fullStars) + '\u2606'.repeat(5 - fullStars);
    }
}

// ========================================
// FAQ Accordion
// ========================================
class FAQManager {
    constructor() {
        this.faqItems = document.querySelectorAll('.faq-item');
        this.init();
    }

    init() {
        this.faqItems.forEach(item => {
            const question = item.querySelector('.faq-question');
            if (question) {
                question.addEventListener('click', () => this.toggleFAQ(item));
            }
        });
    }

    toggleFAQ(item) {
        const isActive = item.classList.contains('active');

        this.faqItems.forEach(faq => {
            faq.classList.remove('active');
            const btn = faq.querySelector('.faq-question');
            if (btn) btn.setAttribute('aria-expanded', 'false');
        });

        if (!isActive) {
            item.classList.add('active');
            item.querySelector('.faq-question').setAttribute('aria-expanded', 'true');
        }
    }
}

// ========================================
// Newsletter Forms
// ========================================
class NewsletterManager {
    constructor() {
        this.forms = document.querySelectorAll('[id*="newsletter-form"], .footer-newsletter-form, .sticky-newsletter-form');
        this.init();
    }

    init() {
        this.forms.forEach(form => {
            form.addEventListener('submit', (e) => this.handleSubmit(e));
        });
    }

    handleSubmit(e) {
        e.preventDefault();
        const form = e.target;
        const emailInput = form.querySelector('input[type="email"]');
        const email = emailInput?.value;

        if (this.validateEmail(email)) {
            console.log('Newsletter signup:', email);
            const btn = form.querySelector('button[type="submit"]');
            const originalText = btn.textContent;
            btn.textContent = 'Subscribed!';
            btn.style.background = 'var(--success-color)';
            form.reset();
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
            }, 3000);
        } else {
            alert('Please enter a valid email address.');
        }
    }

    validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
}

// ========================================
// Sticky Newsletter
// ========================================
class StickyNewsletter {
    constructor() {
        this.stickyBar = document.getElementById('sticky-newsletter');
        this.closeBtn = this.stickyBar?.querySelector('.sticky-newsletter-close');
        this.hasShown = localStorage.getItem('newsletter-shown') === 'true';
        this.init();
    }

    init() {
        if (!this.stickyBar) return;

        window.addEventListener('scroll', () => this.handleScroll(), { passive: true });

        if (this.closeBtn) {
            this.closeBtn.addEventListener('click', () => this.close());
        }
    }

    handleScroll() {
        if (this.hasShown) return;

        const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;

        if (scrollPercent > 50) {
            this.show();
        }
    }

    show() {
        this.stickyBar.classList.add('visible');
        this.hasShown = true;
        localStorage.setItem('newsletter-shown', 'true');
    }

    close() {
        this.stickyBar.classList.remove('visible');
    }
}

// ========================================
// Contact Form
// ========================================
class ContactForm {
    constructor() {
        this.form = document.getElementById('contact-form');
        this.init();
    }

    init() {
        if (!this.form) return;
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    handleSubmit(e) {
        e.preventDefault();

        const formData = {
            name: this.form.querySelector('#contact-name').value,
            email: this.form.querySelector('#contact-email').value,
            subject: this.form.querySelector('#contact-subject').value,
            message: this.form.querySelector('#contact-message').value
        };

        if (!this.validateForm(formData)) return;

        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Sending...';
        submitBtn.disabled = true;

        setTimeout(() => {
            alert('Thank you for your message! We\'ll get back to you within 48 hours.');
            this.form.reset();
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }, 1000);
    }

    validateForm(data) {
        if (!data.name || !data.email || !data.subject || !data.message) {
            alert('Please fill in all fields.');
            return false;
        }

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
            alert('Please enter a valid email address.');
            return false;
        }

        return true;
    }
}

// ========================================
// Smooth Scrolling
// ========================================
class SmoothScroll {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', (e) => {
                const href = anchor.getAttribute('href');
                if (href === '#' || href === '') return;

                const target = document.querySelector(href);
                if (target) {
                    e.preventDefault();
                    const offsetTop = target.offsetTop - 100;
                    window.scrollTo({ top: offsetTop, behavior: 'smooth' });
                }
            });
        });
    }
}

// ========================================
// Lazy Loading Images
// ========================================
class LazyLoader {
    constructor() {
        this.init();
    }

    init() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
}

// ========================================
// Breadcrumb Manager
// ========================================
class BreadcrumbManager {
    constructor() {
        this.breadcrumbs = document.querySelector('.breadcrumbs ol');
        this.init();
    }

    init() {
        const categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) {
            categoryFilter.addEventListener('change', (e) => {
                this.updateBreadcrumbs(e.target.value);
            });
        }
    }

    updateBreadcrumbs(category) {
        if (!this.breadcrumbs) return;

        if (category === 'all') {
            this.breadcrumbs.innerHTML = '<li><a href="/">Home</a></li>';
        } else {
            const label = categoryData[category]?.label || category;
            this.breadcrumbs.innerHTML = `
                <li><a href="/">Home</a></li>
                <li><a href="#categories">Categories</a></li>
                <li>${label}</li>
            `;
        }
    }
}

// ========================================
// Back to Top Button
// ========================================
class BackToTop {
    constructor() {
        this.button = document.getElementById('back-to-top');
        this.init();
    }

    init() {
        if (!this.button) return;

        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                this.button.classList.add('visible');
            } else {
                this.button.classList.remove('visible');
            }
        }, { passive: true });

        this.button.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
}

// ========================================
// Quick Pick Tabs
// ========================================
class QuickPickTabs {
    constructor(data) {
        this.data = data;
        this.container = document.getElementById('quick-picks-container');
        this.init();
    }

    init() {
        if (!this.container) return;
        const tabs = this.container.querySelectorAll('.quick-pick-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                this.showPick(tab.dataset.category);
            });
        });

        // Show first tab
        if (tabs.length > 0) {
            this.showPick(tabs[0].dataset.category);
        }
    }

    showPick(category) {
        const content = this.container.querySelector('.quick-pick-content');
        if (!content) return;

        const topTool = this.data
            .filter(t => t.category === category)
            .sort((a, b) => b.rating - a.rating)[0];

        if (!topTool) {
            content.innerHTML = '<p>No tools in this category yet.</p>';
            return;
        }

        content.innerHTML = `
            <div class="quick-pick-card">
                <img src="${topTool.image}" alt="${topTool.name}" loading="lazy" width="400" height="300">
                <div class="quick-pick-info">
                    <span class="quick-pick-label">${topTool.bestFor || 'Our Top Pick'}</span>
                    <h3>${topTool.name}</h3>
                    <div class="quick-pick-rating">${this.generateStars(topTool.rating)} ${topTool.rating}/5</div>
                    <p>${topTool.excerpt}</p>
                    <div class="quick-pick-pros">
                        ${topTool.pros ? topTool.pros.map(p => `<span class="pro-item">+ ${p}</span>`).join('') : ''}
                    </div>
                    <div class="quick-pick-actions">
                        <span class="quick-pick-price">$${topTool.price.toFixed(2)}</span>
                        <a href="#" class="btn btn-primary btn-small">Check Price on Amazon</a>
                        <a href="#" class="btn btn-secondary btn-small">Full Review</a>
                    </div>
                </div>
            </div>
        `;
    }

    generateStars(rating) {
        const full = Math.floor(rating);
        return '\u2605'.repeat(full) + '\u2606'.repeat(5 - full);
    }
}

// ========================================
// Initialize Everything
// ========================================
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
    new MobileMenu();
    new DropdownNav();
    new SearchManager(toolsData);
    new ReviewsManager(toolsData);
    new ComparisonManager(toolsData);
    new FAQManager();
    new NewsletterManager();
    new StickyNewsletter();
    new ContactForm();
    new SmoothScroll();
    new LazyLoader();
    window.breadcrumbManagerInstance = new BreadcrumbManager();
    new BackToTop();
    new QuickPickTabs(toolsData);

    console.log('ToolShed Tested v2.0 initialized — 24 tools, 6 categories');
});

// ========================================
// Performance Monitoring
// ========================================
if ('performance' in window) {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                console.log('Page Load Time:', Math.round(perfData.loadEventEnd - perfData.fetchStart), 'ms');
            }
        }, 0);
    });
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        ThemeManager,
        SearchManager,
        ReviewsManager,
        ComparisonManager,
        toolsData,
        categoryData
    };
}
