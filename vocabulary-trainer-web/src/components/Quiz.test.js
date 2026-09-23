import { fireEvent, render, screen } from '@testing-library/react';
import Quiz, { normalizeAnswer } from './Quiz';

describe('normalizeAnswer', () => {
  test('accepts apostrophe variants from different keyboards and platforms', () => {
    const expected = "j'habite";
    const variants = [
      "j'habite",
      'j\u2018habite',
      'j\u2019habite',
      'j\u201Bhabite',
      'j\u02BBhabite',
      'j\u02BChabite',
      'j\u2032habite',
      'j\u2035habite',
      'j\u00B4habite',
      'j`habite',
      'j\uFF07habite',
    ];

    variants.forEach((variant) => {
      expect(normalizeAnswer(variant)).toBe(expected);
    });
  });

  test('also normalizes case and repeated whitespace', () => {
    expect(normalizeAnswer("  J’HABITE   ")).toBe("j'habite");
  });

  test('keeps meaningful punctuation differences', () => {
    expect(normalizeAnswer('j-habite')).not.toBe("j'habite");
    expect(normalizeAnswer('j"habite')).not.toBe("j'habite");
  });
});

test('returns directly from an active quiz to Quiz Oppsett', () => {
  render(
    <Quiz
      onNavigate={jest.fn()}
      vocabulary={[{ week: 1, norwegian: 'hus', english: 'house' }]}
      username="Test"
      saveScore={jest.fn()}
      language="english"
      languageLabel="Engelsk"
    />
  );

  fireEvent.click(screen.getByRole('button', { name: /start quiz/i }));
  fireEvent.click(screen.getByRole('button', { name: /quiz oppsett/i }));

  expect(screen.getByRole('heading', { name: /quiz oppsett/i })).toBeInTheDocument();
});