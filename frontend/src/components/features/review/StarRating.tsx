"use client";

import { useState } from "react";
import { Star } from "lucide-react";
import { formatarNota } from "@/lib/rating";

type StarRatingProps = {
  value: number | null;
  // Sem onChange = so leitura (media no banner, nota no comentario).
  // Com onChange = interativo (formulario).
  onChange?: (nota: number) => void;
  size?: number;
  vazioClassName?: string;
  cheioClassName?: string;
};

export function StarRating({
  value,
  onChange,
  size = 20,
  vazioClassName = "text-gray-300",
  cheioClassName = "text-amber-500",
}: StarRatingProps) {
  // Nota sob o mouse, so pra pre-visualizar antes de clicar.
  const [hover, setHover] = useState<number | null>(null);
  const interativo = !!onChange;
  const exibida = hover ?? value ?? 0;

  return (
    <div
      className="inline-flex"
      role={interativo ? "radiogroup" : "img"}
      aria-label={value !== null ? `Nota ${formatarNota(value)} de 5` : "Sem nota"}
      onMouseLeave={() => setHover(null)}
    >
      {[1, 2, 3, 4, 5].map((estrela) => {
        // 0, 0.5 ou 1: quanto desta estrela fica preenchida.
        const preenchimento = Math.max(0, Math.min(1, exibida - (estrela - 1)));

        return (
          <span
            key={estrela}
            className="relative inline-block shrink-0"
            style={{ width: size, height: size }}
          >
            {/* Camada de baixo: contorno da estrela vazia. */}
            <Star size={size} className={`absolute inset-0 ${vazioClassName}`} />

            {/* Camada de cima: estrela cheia, cortada na largura certa. */}
            <span
              className="absolute inset-y-0 left-0 overflow-hidden"
              style={{ width: `${preenchimento * 100}%` }}
            >
              <Star
                size={size}
                className={`fill-current ${cheioClassName}`}
                style={{ maxWidth: "none" }}
              />
            </span>

            {/* Duas areas clicaveis por estrela: metade esquerda = x,5 e
                metade direita = nota inteira. */}
            {interativo &&
              [estrela - 0.5, estrela].map((nota, i) => (
                <button
                  key={nota}
                  type="button"
                  role="radio"
                  aria-checked={value === nota}
                  aria-label={`${formatarNota(nota)} estrelas`}
                  onMouseEnter={() => setHover(nota)}
                  onFocus={() => setHover(nota)}
                  onBlur={() => setHover(null)}
                  onClick={() => onChange(nota)}
                  className={`absolute inset-y-0 w-1/2 ${i === 0 ? "left-0" : "right-0"}`}
                />
              ))}
          </span>
        );
      })}
    </div>
  );
}