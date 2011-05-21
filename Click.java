import java.awt.Robot;
import java.awt.event.InputEvent;

public class Click{

   public static void main(String args[]){
	try{
		Robot robot1 = new Robot();
		
		while(true){
 			robot1.mousePress(InputEvent.BUTTON1_MASK);
 			robot1.mouseRelease(InputEvent.BUTTON1_MASK);
			robot1.delay(3000);	//Wait for 3 seconds
		}
   	}catch(Exception e){
		System.out.println(e.getMessage());
	}
   }
}
