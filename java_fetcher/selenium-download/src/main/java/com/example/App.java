package com.example;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        System.setProperty("webdriver.chrome.driver", "C:\\tools\\chromedriver-win64\\chromedriver.exe");
        String downloadFilepath = "D:\\projects\\finance_project\\downloads";
        Map<String, Object> prefs = new HashMap<>();
        prefs.put("download.default_directory", downloadFilepath);
        prefs.put("download.prompt_for_download", false);
        ChromeOptions options = new ChromeOptions();
        options.setExperimentalOption("prefs", prefs);
        WebDriver driver = new ChromeDriver(options);
        String[] companyCodes = {
            "ADANIPORTS","ASIANPAINT","AXISBANK","BAJAJ-AUTO","BAJFINANCE","BAJAJFINSV","BPCL","BHARTIARTL",
            "BRITANNIA","CIPLA","COALINDIA","DIVISLAB","DRREDDY","EICHERMOT","GRASIM","HCLTECH","HDFCBANK",
            "HDFCLIFE","HEROMOTOCO","HINDALCO","HINDUNILVR","ICICIBANK","INDUSINDBK","INFY","ITC","JSWSTEEL",
            "KOTAKBANK","LTIM","LT","M&M","MARUTI","NESTLEIND","NTPC","ONGC","POWERGRID","RELIANCE","SBILIFE",
            "SBIN","SHREECEM","SUNPHARMA","TATACONSUM","TATAMOTORS","TATASTEEL","TCS","TECHM","TITAN",
            "ULTRACEMCO","UPL","WIPRO"
        };

         String[][] companies = {
            {"ADANIPORTS", "6594426"},
            {"ASIANPAINT", "6594812"},
            {"AXISBANK", "6594837"},
            {"ADANIENT","6594425"},
            {"APOLLOHOSP","6594634"},
            {"BAJAJ-AUTO", "6594849"},
            {"BAJFINANCE", "6594851"},
            {"BEL", "6595017"},
            {"BHARTIARTL", "6595023"},
            {"CIPLA", "6595253"},
            {"COALINDIA", "6595259"},
            {"DRREDDY", "6595620"},
            {"EICHERMOT", "6595636"},
            {"ETERNAL","68088707"},
            {"GRASIM", "6596053"},
            {"HCLTECH", "6596236"},
            {"HDFCBANK", "6596237"},
            {"HDFCLIFE", "17832651"},
            {"HEROMOTOCO", "6596243"},
            {"HINDALCO", "6596253"},
            {"HINDUNILVR", "6596263"},
            {"ICICIBANK", "6596413"},
            {"INDUSINDBK", "9695129"},
            {"INFY", "6596470"},
            {"ITC", "6596626"},
            {"JSWSTEEL", "6596816"},
            {"JIOFIN", "106186007"},
            {"KOTAKBANK", "6597025"},
            {"LT", "6597052"},
            {"M&M", "6597229"},
            {"MARUTI", "6597252"},
            {"NESTLEIND", "128275928"},
            {"NTPC", "6597657"},
            {"ONGC", "6597668"},
            {"POWERGRID", "6598025"},
            {"RELIANCE", "6598251"},
            {"SBILIFE", "17087873"},
            {"SHRIRAMFIN","6598665"},
            {"SBIN", "6598877"},
            {"SUNPHARMA", "6599038"},
            {"TATACONSUM", "6599232"},
            {"TATAMOTORS", "6599235"},
            {"TATASTEEL", "6599238"},
            {"TRENT","6599419"},
            {"TCS", "6599230"},
            {"TECHM", "6599866"},
            {"TITAN", "6599273"},
            {"ULTRACEMCO", "6599447"},
            {"WIPRO", "6599824"}
        };


        try {
            //login
            // 1. Go to login page
            driver.get("https://www.screener.in/login/");
            // 2. Enter username and password
            driver.findElement(By.name("username")).sendKeys("bansalrajan553@gmail.com");
            driver.findElement(By.name("password")).sendKeys("Xdr%553@rb");
            // 3. Submit the login form
            driver.findElement(By.cssSelector("form button[type='submit']")).click();
            // 4. Wait for login to complete (adjust as needed)
            Thread.sleep(5000);

            //String[][] companies = CompanyCodeGetter.getExportIds(driver, companyCodes);

            for (String[] company : companies) {
                // String url = String.format("https://www.screener.in/company/%s/consolidated/", code);
                // driver.get(url);

                // // Wait for page to load
                // Thread.sleep(2000);
                String code = company[0];
                String exportId = company[1];
                if (exportId.equals("NOT_FOUND")) {
                    System.out.println("Skipping " + code + " (export ID not found)");
                    continue;
                }
                String url = String.format("https://www.screener.in/company/%s/consolidated/", code);
                driver.get(url);
                Thread.sleep(2000);

                try {
                    String buttonXpath = String.format("//button[@formaction='/user/company/export/%s/']", exportId);
                    driver.findElement(By.xpath(buttonXpath)).click();
                    System.out.println("Download triggered for: " + code);
                } catch (Exception ex) {
                    System.out.println("Failed to download for: " + code + " (button not found or error)");
                }
                Thread.sleep(10000);

                
            }

            // 7. Wait for the download to complete
            //Thread.sleep(5000);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            driver.quit();
        }
    }
    }

