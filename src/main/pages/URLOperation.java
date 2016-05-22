package pages;
import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public class URLOperation {
    private static final Logger logger = Logger.getLogger(URLOperation.class.getName());


    public String parseURL(String inputUrl) {
        String retFile = null;
        URLConnection urlConnection;
        URL url = null;

        try {
            url = new URL(inputUrl);
        } catch (MalformedURLException e) {
            e.printStackTrace();
        }


        try {
            assert url != null;
            urlConnection = url.openConnection();
            java.io.InputStream in = urlConnection.getInputStream();
            BufferedReader br = new BufferedReader(new InputStreamReader(in));
            StringBuilder file = new StringBuilder();
            String tmp;
            while((tmp = br.readLine()) != null) {
                file.append(tmp).append("\n");
            }
            retFile = file.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }
        logger.info("load successfully");
        return retFile;
    }

    public static void main(String[] args) {
        String testUrl = "http://www.baidu.com";
        //DOMConfigurator.configure("log4j.properties");
        logger.info("load successfully");

        //System.out.println(new URLOperation().parseURL(testUrl));


    }
}
