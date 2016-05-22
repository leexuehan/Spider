package downloader;
import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

public class URLParser {
    private static final Logger logger = Logger.getLogger(URLParser.class.getName());


    public String parse(String inputUrl) {
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
        return retFile;
    }

}
