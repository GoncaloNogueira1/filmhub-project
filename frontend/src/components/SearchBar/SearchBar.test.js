import { render, screen, fireEvent } from '@testing-library/react';
import SearchBar from './SearchBar';

describe('SearchBar', () => {
    const mockOnSearch = jest.fn();

    beforeEach(() => {
        mockOnSearch.mockClear();
    });

    it('renders input with placeholder', () => {
        render(<SearchBar onSearch={mockOnSearch} placeholder="Test Placeholder" />);
        expect(screen.getByPlaceholderText('Test Placeholder')).toBeInTheDocument();
    });

    it('updates input value on change', () => {
        render(<SearchBar onSearch={mockOnSearch} />);
        const input = screen.getByRole('textbox');
        fireEvent.change(input, { target: { value: 'Inception' } });
        expect(input.value).toBe('Inception');
    });

    it('calls onSearch with query on submit', () => {
        render(<SearchBar onSearch={mockOnSearch} />);
        const input = screen.getByRole('textbox');
        const button = screen.getByText('Search');

        fireEvent.change(input, { target: { value: '  Matrix  ' } }); // Test trimming
        fireEvent.click(button);

        expect(mockOnSearch).toHaveBeenCalledWith('Matrix');
    });

    it('does not call onSearch if query is empty', () => {
        render(<SearchBar onSearch={mockOnSearch} />);
        const button = screen.getByText('Search');
        fireEvent.click(button);
        expect(mockOnSearch).not.toHaveBeenCalled();
    });

    it('clears input and search when clear button is clicked', () => {
        render(<SearchBar onSearch={mockOnSearch} />);
        const input = screen.getByRole('textbox');
        
        // Type something to make clear button appear
        fireEvent.change(input, { target: { value: 'Test' } });
        expect(input.value).toBe('Test');
        
        const clearBtn = screen.getByText('✕');
        fireEvent.click(clearBtn);
        
        expect(input.value).toBe('');
        expect(mockOnSearch).toHaveBeenCalledWith('');
    });
});
