package org.example.kingdomdefense;

import org.libsdl.app.SDLActivity;

public class KingdomDefenseActivity extends SDLActivity {
    
    @Override
    protected String[] getLibraries() {
        return new String[] {
            "SDL2",
            "SDL2_image",
            "SDL2_mixer",
            "SDL2_ttf",
            "python3.8",
            "pygame"
        };
    }
    
    @Override
    protected String getMainScript() {
        return "main.py";
    }
}