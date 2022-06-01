import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SaltminionsComponent } from './saltminions.component';

describe('SaltminionsComponent', () => {
  let component: SaltminionsComponent;
  let fixture: ComponentFixture<SaltminionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SaltminionsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SaltminionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
