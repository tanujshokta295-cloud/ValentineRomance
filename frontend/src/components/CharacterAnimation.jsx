import { useState } from 'react';
import { Player } from '@lottiefiles/react-lottie-player';

const characters = {
  panda: {
    name: 'Cute Panda',
    lottieUrl: 'https://lottie.host/e1e68e5a-44a5-4a8e-8c1e-90f4f239f60f/BKqAJ58qKQ.json',
    fallbackImage: null,
    fallbackEmoji: '🐼',
  },
  bear: {
    name: 'Teddy Bear',
    lottieUrl: null, // No working lottie, use image
    fallbackImage: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
    fallbackEmoji: '🧸',
  },
  bunny: {
    name: 'Love Bunny',
    lottieUrl: null, // No working lottie, use image
    fallbackImage: 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
    fallbackEmoji: '🐰',
  },
};

const CharacterAnimation = ({ characterType = 'panda', className = '' }) => {
  const [lottieError, setLottieError] = useState(false);
  const character = characters[characterType] || characters.panda;

  const handleLottieError = () => {
    setLottieError(true);
  };

  // Show fallback if no lottie URL or if lottie failed to load
  const showFallback = !character.lottieUrl || lottieError;

  return (
    <div className={`character-container bounce-soft ${className}`}>
      {!showFallback ? (
        <Player
          autoplay
          loop
          src={character.lottieUrl}
          style={{ width: '100%', height: '100%' }}
          onEvent={(event) => {
            if (event === 'error') {
              handleLottieError();
            }
          }}
        />
      ) : (
        <div className="w-full h-full flex items-center justify-center">
          {character.fallbackImage ? (
            <img 
              src={character.fallbackImage} 
              alt={character.name}
              className="w-full h-full object-cover rounded-2xl shadow-lg"
              onError={() => {
                // If image also fails, we'll still have the container
              }}
            />
          ) : (
            <span className="text-8xl">{character.fallbackEmoji}</span>
          )}
        </div>
      )}
    </div>
  );
};

export { characters };
export default CharacterAnimation;
