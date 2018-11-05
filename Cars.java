/*A class called Cars with variables: 
 * colours, make, models and two constructors: 
 * a default constructor and one that has colour, 
 * make and models in its arguments
- Set up the getters/setters for each of the variables
- Create a method to take another car’s colour
- In the main, create two different cars with different colours, 
  make and model*/

public class Cars {
       public  String colors ;
       private String make;
       private String models ;
    //default constructor, the variables could set some default values
	public Cars() {
	}
	// this is constructor take arguments
	public Cars(String colors, String make, String models) {
		this.colors = colors;
		this.make = make;
		this.models = models;
	}
	// this takes an object 
	public Cars(Cars obj) {
		colors=obj.colors;
	}
	// getter and setter
    public String getColors() {
		return colors;
	}
	public void setColors(String colors) {
		this.colors = colors;
	}
	public String getMake() {
		return make;
	}
	public void setMake(String make) {
		this.make = make;
	}
	public String getModels() {
		return models;
	}
	public void setModels(String models) {
		this.models = models;
	}
	//a method to take another car’s colour
	public  void getCarcolors(Cars obj){
		System.out.println("The color of another car is " + obj.colors); 
		
	}
	// display method
	void display() {
		System.out.println("New car is "+colors+" "+make+" "+models);
		}
	// the main method
	public static void main(String[] args)  {
    	Cars car1= new Cars();
    	// Initialising object by reference variable
    	car1.colors="Black";
    	car1.make="Audi";
    	car1.models="Q8";
    	// Initialising object by constructor
    	Cars car2= new Cars("Red","BMW","X5");
        car1.display();
        car2.display();
        
        // get another car's colour
        car1.getCarcolors(car2);
    	
    } 
}




