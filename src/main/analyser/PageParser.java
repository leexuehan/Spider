package analyser;

import downloader.URLDownloader;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class PageParser {
    public static void analyse(String pages){
        Document doc = Jsoup.parseBodyFragment(pages);
        String title = doc.title();
        String text = doc.text();
        System.out.println(title);
        System.out.println(text);
    }

    public static void main(String[] args) {
        analyse(new URLDownloader().getPages("http://www.baidu.com"));
    }
}
