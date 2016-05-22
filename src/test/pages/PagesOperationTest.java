package pages;

import org.apache.log4j.Logger;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class PagesOperationTest {
    Logger logger = Logger.getLogger(this.getClass().getName());

    @Before
    public void setUp() {
    }

    @After
    public void tearDown() {
    }

    @Test
    public void should_return_200_ok_when_url_given() {
        String testUrl = "http://www.baidu.com";
        String localFilePath = "/Users/lixuehan/Spider/Spider/src/test/TestResources/DemoPage.html";
        String expectedFile;
        String actualFile;

        //expectedFile = getLocalFile(localFilePath);
        actualFile = new URLOperation().parseURL(testUrl);
        logger.info(actualFile);

        //assertThat(actualFile).isEqualTo(expectedFile);
    }


}
