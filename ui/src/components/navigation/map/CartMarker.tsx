import { type Coordinate } from "~/types/Navigation";

interface CartMarkerProps {
    pos: Coordinate
    heading: number
}

export default function CartMarker({pos, heading}: CartMarkerProps) {
  const style = {
    transform: `translate(-50%, -50%) rotate(${heading}deg)`,
    left: `${pos.x}px`,
    top: `${pos.y}px`,
  };

  return (
    <div
      className="absolute flex items-center justify-center"
      style={style} // Applying dynamic styles for rotation and positioning
    >
      <span
        className="text-2xl" // Using Tailwind's text size scale
      >
        ⏫
      </span>
    </div>
  );
}
