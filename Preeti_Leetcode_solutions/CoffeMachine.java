package Preeti;

-----------------------------
Constant.java
-----------------------------
package lld.coffevending;

public class Constant {

    public enum DRINKS {
        CAPPUCCINO, ESPRESSO, AMERICANO;
    }
}

-----------------------------
Recipe.java
-----------------------------
package lld.coffevending;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public class Recipe {

    private List<String> instructionList;
    Map<Ingredient, Integer> ingredientMap = new LinkedHashMap<>();

    public Map<Ingredient, Integer> getIngredientMap() {
        return this.ingredientMap;
    }

    public List<String> getInstructionList() {
        return instructionList;
    }

    public void setInstructionList(List<String> instructionList) {
        this.instructionList = instructionList;
    }

    public void addIngredient(Ingredient ingredient, int ingredientAmount) {
        this.ingredientMap.put(ingredient, ingredientAmount);
    }

    @Override
    public String toString() {
        return "Recipe{" +
                "instructionList=" + instructionList +
                ", ingredientMap=" + ingredientMap +
                '}';
    }
}

-----------------------------
Drink.java
-----------------------------
package lld.coffevending;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public abstract class Drink {

    String drinkName;
    Recipe recipe;
    Double price;
    Mixer mixer;
    Map<Ingredient, Integer> commonIngredient;

    public Drink(String drinkName) {
        this.drinkName = drinkName;
    }

    public Drink(String drinkName, Recipe recipe, Double price, Mixer mixer) {
        this.drinkName = drinkName;
        this.recipe = recipe;
        this.price = price;
        this.mixer = mixer;
    }

    public abstract Drink process();

    public abstract void addCommonIngredient(Ingredient ingredient, int volume);

    public Map<Ingredient, Integer> getWholeIngredient(Map<Ingredient, Integer> drinkSpecificIngredientMap) {
        Map<Ingredient, Integer> map = new LinkedHashMap<>(drinkSpecificIngredientMap);
        map.putAll(commonIngredient);
        return map;
    }
}

-----------------------------
Americano.java
-----------------------------
package lld.coffevending;

import java.util.Map;

public class Americano extends Drink {

    public Americano(String drinkName) {
        super(drinkName);
    }

    public Americano(String drinkName, Recipe recipe, Double price, Mixer mixer) {
        super(Constant.DRINKS.AMERICANO.name(), recipe, price, mixer);
    }

    @Override
    public Americano process() {
        Map<Ingredient, Integer> ingredientMap = getWholeIngredient(recipe.getIngredientMap());
        Americano americano = (Americano) mixer.makeDrink(this.drinkName, recipe.getInstructionList(), ingredientMap);
        americano.price = this.price;
        americano.recipe = this.recipe;
        return americano;
    }

    @Override
    public void addCommonIngredient(Ingredient ingredient, int volume) {
        this.commonIngredient.put(ingredient, volume);
    }

    @Override
    public String toString() {
        return "Americano{" +
                "drinkName='" + drinkName + '\'' +
                ", recipe=" + recipe +
                ", price=" + price +
                '}';
    }
}

-----------------------------
Cappuccino.java
-----------------------------
package lld.coffevending;

import java.util.Map;

public class Cappuccino extends Drink {

    public Cappuccino(String drinkName) {
        super(drinkName);
    }

    public Cappuccino(String drinkName, Recipe recipe, Double price, Mixer mixer) {
        super(Constant.DRINKS.CAPPUCCINO.name(), recipe, price, mixer);
    }

    @Override
    public Cappuccino process() {
        Map<Ingredient, Integer> ingredientMap = getWholeIngredient(recipe.getIngredientMap());
        Cappuccino cappuccino = (Cappuccino) mixer.makeDrink(this.drinkName, recipe.getInstructionList(), ingredientMap);
        cappuccino.price = this.price;
        cappuccino.recipe = this.recipe;
        return cappuccino;
    }

    @Override
    public void addCommonIngredient(Ingredient ingredient, int volume) {
        this.commonIngredient.put(ingredient, volume);
    }

    @Override
    public String toString() {
        return "Cappuccino{" +
                "drinkName='" + drinkName + '\'' +
                ", recipe=" + recipe +
                ", price=" + price +
                '}';
    }
}
-----------------------------
Espresso.java
-----------------------------
package lld.coffevending;

import java.util.Map;

public class Espresso extends Drink {

    String extraIngredient;

    public Espresso(String drinkName) {
        super(drinkName);
    }

    public Espresso(String drinkName, Recipe recipe, Double price, Mixer mixer) {
        super(Constant.DRINKS.ESPRESSO.name(), recipe, price, mixer);
        this.extraIngredient = "added cream";
    }

    @Override
    public Espresso process() {
        Map<Ingredient, Integer> ingredientMap = getWholeIngredient(recipe.getIngredientMap());
        Espresso espresso = (Espresso) mixer.makeDrink(this.drinkName, recipe.getInstructionList(), ingredientMap);
        espresso.price = this.price;
        espresso.recipe = this.recipe;
        return espresso;
    }

    @Override
    public void addCommonIngredient(Ingredient ingredient, int volume) {
        this.commonIngredient.put(ingredient, volume);
    }

    @Override
    public String toString() {
        return "Espresso{" +
                "extraIngredient='" + extraIngredient + '\'' +
                ", drinkName='" + drinkName + '\'' +
                ", recipe=" + recipe +
                ", price=" + price +
                '}';
    }
}

-----------------------------
Ingredient.java
-----------------------------
package lld.coffevending;

import java.util.Objects;

public class Ingredient {

    String name;

    public Ingredient(String name) {
        this.name = name;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Ingredient that = (Ingredient) o;
        return Objects.equals(name, that.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }

    @Override
    public String toString() {
        return "Ingredient{" +
                "name='" + name + '\'' +
                '}';
    }
}

-----------------------------
Water.java
-----------------------------
package lld.coffevending;

public class Water extends Ingredient {

    public Water(String name) {
        super(name);
    }
}

-----------------------------
IngredientInventory.java
-----------------------------
package lld.coffevending;

import java.util.HashMap;
import java.util.Map;

public class IngredientInventory {

    Map<Ingredient, Integer> ingredientInventoryMap = new HashMap<>();

    public void addIngredient(Ingredient ingredient, int volume) {
        ingredientInventoryMap.put(ingredient, volume);
    }

    public boolean getIngredient(Ingredient ingredient, int requestedVolume) {
        if (!ingredientInventoryMap.containsKey(ingredient)) {
            throw new RuntimeException("Ingredient " + ingredient.name + " Not Found!!");
        }
        int curVolume = ingredientInventoryMap.getOrDefault(ingredient, 0);
        if (curVolume < requestedVolume) {
            throw new RuntimeException("Insufficient amount of ingredient!! : " + ingredient.name);
        }
        curVolume = (curVolume - requestedVolume);
        ingredientInventoryMap.put(ingredient, curVolume);
        if (curVolume < 10) {
            sendAlert(ingredient);
        }
        return true;
    }

    // send alert to admin
    private void sendAlert(Ingredient ingredient) {
    }
}

-----------------------------
Mixer.java
-----------------------------
package lld.coffevending;

import java.util.List;
import java.util.Map;

public class Mixer {

    private IngredientInventory ingredientInventory;

    public Mixer(IngredientInventory ingredientInventory) {
        this.ingredientInventory = ingredientInventory;
    }

    public Drink makeDrink(String drinkName, List<String> instructionList, Map<Ingredient, Integer> ingredientMap) {
        for (Ingredient ingredient : ingredientMap.keySet()) {
            if (ingredientInventory.getIngredient(ingredient, ingredientMap.get(ingredient))) {
                continue;
            }
        }
        if (drinkName.equals(Constant.DRINKS.CAPPUCCINO)) {
            return new Cappuccino(drinkName);
        } else if (drinkName.equals(Constant.DRINKS.AMERICANO)) {
            return new Americano(drinkName);
        } else if (drinkName.equals(Constant.DRINKS.ESPRESSO)) {
            return new Espresso(drinkName);
        }
        return null;
    }
}
