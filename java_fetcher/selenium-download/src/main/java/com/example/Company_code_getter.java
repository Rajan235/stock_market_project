package com.example;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Company_code_getter {

     public static String[][] getExportIds(WebDriver driver, String[] companyCodes) throws InterruptedException {
        String[][] companies = new String[companyCodes.length][2];

        for (int i = 0; i < companyCodes.length; i++) {
            String code = companyCodes[i];
            String url = String.format("https://www.screener.in/company/%s/consolidated/", code);
            driver.get(url);
            Thread.sleep(2000);

            try {
                String formaction = driver.findElement(By.cssSelector("button[formaction*='/user/company/export/']")).getAttribute("formaction");
                Pattern p = Pattern.compile("/user/company/export/(\\d+)/");
                Matcher m = p.matcher(formaction);
                if (m.find()) {
                    companies[i][0] = code;
                    companies[i][1] = m.group(1);
                } else {
                    companies[i][0] = code;
                    companies[i][1] = "NOT_FOUND";
                }
            } catch (Exception e) {
                companies[i][0] = code;
                companies[i][1] = "NOT_FOUND";
            }
            Thread.sleep(2000);
        }
        return companies;
    }

}
