const puppeteer = require('puppeteer');

const CONFIG = {
    APPNAME: process.env['APPNAME'] || "Admin",
    APPURL: process.env['APPURL'] || "http://172.25.0.3:3000",
    APPHOST: process.env['APPHOST'] || "172.25.0.3",
    APPLIMITTIME: Number(process.env['APPLIMITTIME'] || "60"),
    APPLIMIT: Number(process.env['APPLIMIT'] || "5"),
    ADMIN_USERNAME: process.env['ADMIN_USERNAME'] || "admin",
    ADMIN_PASSWORD: process.env['ADMIN_PASSWORD'] || "admin"
};

console.table(CONFIG);

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function initBrowser() {
    return await puppeteer.launch({
        executablePath: "/usr/bin/chromium-browser",
        headless: true,
        args: [
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--no-gpu',
            '--disable-default-apps',
            '--disable-translate',
            '--disable-device-discovery-notifications',
            '--disable-software-rasterizer',
            '--disable-xss-auditor'
        ],
        ignoreHTTPSErrors: true
    });
}

console.log("Bot started...");

async function adminLogin(browser) {
    const context = await browser.createIncognitoBrowserContext();
    const page = await context.newPage();

    try {
        console.log("Logging in as admin...");
        await page.goto(`${CONFIG.APPURL}/login`, { waitUntil: "networkidle2" });
        // Fill the login form
        await page.type('input[name="username"]', CONFIG.ADMIN_USERNAME);
        await page.type('input[name="password"]', CONFIG.ADMIN_PASSWORD);
        await page.click('button[type="submit"]');

        // Wait for navigation after login
        console.log(CONFIG.ADMIN_USERNAME);
        

        // Get session cookies
        const cookies = await page.cookies();
        console.log("Admin login successful. Cookies:", cookies);

        await page.close();
        return { context, cookies };
    } catch (err) {
        console.error("Admin login failed:", err);
        await page.close();
        return null;
    }
}

module.exports = {
    name: CONFIG.APPNAME,
    urlRegex: `^${CONFIG.APPURL}/.*$`,
    rateLimit: {
        windowS: CONFIG.APPLIMITTIME,
        max: CONFIG.APPLIMIT
    },
    bot: async (urlToVisit) => {
        const browser = await initBrowser();
        const loginSession = await adminLogin(browser);
        
        if (!loginSession) {
            console.log("Failed to get admin session. Exiting...");
            await browser.close();
            return false;
        }

        const { context, cookies } = loginSession;

        try {
            console.log(`Bot visiting: ${urlToVisit} as admin`);
            const page = await context.newPage();
            await page.setCookie(...cookies);

            await page.goto(urlToVisit, { waitUntil: "networkidle2" });
            await sleep(15000);

            console.log("Done visiting reported page.");
            await browser.close();
            return true;
        } catch (e) {
            console.error(e);
            await browser.close();
            return false;
        }
    }
};
