import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

// Async thunk to fetch tasks from the API
export const fetchTasks = createAsyncThunk("tasks/fetchTasks", async () => {
  const response = await axios.get("http://127.0.0.1:8000/v1/categories"); // Replace with your actual API endpoint
  return response.data;
});

// Add new category (new thunk)
export const addCategory = createAsyncThunk(
  "tasks/addCategory",
  async (categoryName, { rejectWithValue }) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/v1/categories", {
        name: categoryName,
      });
      return response.data;
    } catch (err) {
      return rejectWithValue(err.response.data);
    }
  }
);

// Update category (new thunk)
export const updateCategory = createAsyncThunk(
  "tasks/updateCategory",
  async ({ categoryId, name }, { rejectWithValue }) => {
    try {
      const response = await axios.put(
        `http://127.0.0.1:8000/v1/categories/${categoryId}`,
        { name }
      );
      return response.data;
    } catch (err) {
      return rejectWithValue(err.response.data);
    }
  }
);

// Delete category (new thunk)
export const deleteCategory = createAsyncThunk(
  "tasks/deleteCategory",
  async (categoryId, { rejectWithValue }) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/v1/categories/${categoryId}`);
      return categoryId;
    } catch (err) {
      return rejectWithValue(err.response.data);
    }
  }
);

// Async thunk to add a new task
export const addTask = createAsyncThunk(
  "tasks/addTask",
  async (
    { categoryId, title, description, taskOrder },
    { rejectWithValue }
  ) => {
    try {
      const response = await axios.post(
        `http://127.0.0.1:8000/v1/categories/${categoryId}/tasks`,
        { title, description, task_order: taskOrder }
      );
      return response.data;
    } catch (err) {
      return rejectWithValue(err.response.data);
    }
  }
);

// Async thunk to update an existing task
export const updateTask = createAsyncThunk(
  "tasks/updateTask",
  async (
    { taskId, title, description, taskOrder, categoryId },
    { rejectWithValue }
  ) => {
    try {
      const response = await axios.put(
        `http://127.0.0.1:8000/v1/tasks/${taskId}`,
        { title, description, task_order: taskOrder, category_id: categoryId }
      );
      return response.data;
    } catch (err) {
      return rejectWithValue(err.response.data);
    }
  }
);

// Async thunk to delete a task
export const deleteTask = createAsyncThunk(
  "tasks/deleteTask",
  async (taskId, { rejectWithValue }) => {
    try {
      const response = await axios.delete(`http://127.0.0.1:8000/v1/tasks/${taskId}`);
      return { id: taskId, category_id: response.data.category_id };
    } catch (err) {
      return rejectWithValue(err.response.data);
    }
  }
);

const taskSlice = createSlice({
  name: "tasks",
  initialState: {
    categories: [], // Array to hold categories and tasks
    status: "idle", // Status of the fetch operation
    error: null, // Error message if the fetch fails
  },
  reducers: {
    setCategories: (state, action) => {
      state.categories = action.payload;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => {
        state.status = "loading";
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.status = "succeeded";
        // Assuming API returns data structured as { categories: [...] }
        state.categories = action.payload;
      })
      .addCase(fetchTasks.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.error.message;
      })
      .addCase(addCategory.pending, (state) => {
        state.status = "loading";
      })
      .addCase(addCategory.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.categories.push(action.payload); // Add the new category to the state
      })
      .addCase(addCategory.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload || "Failed to add category";
      })
      .addCase(deleteCategory.pending, (state) => {
        state.status = "loading";
      })
      .addCase(deleteCategory.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.categories = state.categories.filter(
          (category) => category.id !== action.payload
        );
      })
      .addCase(deleteCategory.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload.detail || "Failed to delete category";
      })
      .addCase(updateCategory.pending, (state) => {
        state.status = "loading";
      })
      .addCase(updateCategory.fulfilled, (state, action) => {
        state.status = "succeeded";
        const { id, name } = action.payload;
        const existingCategory = state.categories.find((cat) => cat.id === id);
        if (existingCategory) {
          existingCategory.name = name;
        }
      })
      .addCase(updateCategory.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload.detail || "Failed to update category";
      })
      .addCase(addTask.fulfilled, (state, action) => {
        const { category_id } = action.payload;
        const category = state.categories.find((cat) => cat.id === category_id);
        if (category) {
          category.tasks.push(action.payload);
        }
      })
      .addCase(updateTask.fulfilled, (state, action) => {
        const { id, category_id } = action.payload;
        const category = state.categories.find((cat) => cat.id === category_id);
        if (category) {
          const taskIndex = category.tasks.findIndex((task) => task.id === id);
          if (taskIndex >= 0) {
            category.tasks[taskIndex] = action.payload;
          }
        }
      })
      .addCase(deleteTask.fulfilled, (state, action) => {
        console.log('Task deleted:', action.payload); // Debugging log
        const { id, category_id } = action.payload;
        state.categories = state.categories.map(category => {
          if (category.id === category_id) {
            return {
              ...category,
              tasks: category.tasks.filter((task) => task.id !== id)
            };
          }
          return category;
        });
      })
      .addCase(deleteTask.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload.detail || "Failed to delete task";
      });
  },
});

export const { setCategories } = taskSlice.actions;

export default taskSlice.reducer;
