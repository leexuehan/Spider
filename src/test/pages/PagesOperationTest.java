package pages;

import org.apache.log4j.Logger;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import static org.assertj.core.api.Assertions.assertThat;

public class PagesOperationTest {
    Logger logger = Logger.getLogger(this.getClass().getName());

    @Before
    public void setUp() {
    }

    @After
    public void tearDown() {
    }

    @Test
    public void should_return_correct_title_when_url_given() {
        String testUrl = "http://www.baidu.com";
        String parsedFile = new URLOperation().parseURL(testUrl);
        Document doc = Jsoup.parse(parsedFile);

        String actual = doc.title();
        String expected = "百度一下，你就知道";

        assertThat(actual).isEqualTo(expected);
    }


}
