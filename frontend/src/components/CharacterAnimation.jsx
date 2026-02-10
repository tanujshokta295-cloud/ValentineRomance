import { Player } from '@lottiefiles/react-lottie-player';

const characters = {
  panda: {
    name: 'Cute Panda',
    lottieUrl: 'https://lottie.host/e1e68e5a-44a5-4a8e-8c1e-90f4f239f60f/BKqAJ58qKQ.json',
    fallbackEmoji: '🐼',
  },
  bear: {
    name: 'Teddy Bear',
    lottieUrl: 'https://lottie.host/0e6c9e23-c6c5-4e0e-8d6e-0f9e8f4c5e0f/bear.json',
    fallbackImage: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop',
    fallbackEmoji: '🧸',
  },
  bunny: {
    name: 'Love Bunny',
    lottieUrl: 'https://lottie.host/bunny-love.json',
    fallbackImage: 'https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?w=300&h=300&fit=crop',
    fallbackEmoji: '🐰',
  },
};

const CharacterAnimation = ({ characterType = 'panda', className = '' }) => {
  const character = characters[characterType] || characters.panda;

  return (
    <div className={`character-container bounce-soft ${className}`}>
      <Player
        autoplay
        loop
        src={character.lottieUrl}
        style={{ width: '100%', height: '100%' }}
        onError={() => {
          // Fallback handled by the error boundary or default display
        }}
      >
        {/* Fallback content */}
        <div className="w-full h-full flex items-center justify-center">
          {character.fallbackImage ? (
            <img 
              src={character.fallbackImage} 
              alt={character.name}
              className="w-full h-full object-contain rounded-2xl"
            />
          ) : (
            <span className="text-8xl">{character.fallbackEmoji}</span>
          )}
        </div>
      </Player>
    </div>
  );
};

export { characters };
export default CharacterAnimation;
